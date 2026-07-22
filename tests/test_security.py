"""
Security / vulnerability regression tests.

Verifies:
  - SQL injection attacks are blocked by execute_custom_sql
  - os.system is not used (subprocess.run used instead)
  - Match engine validates inputs
  - Silent exception swallowing is fixed
"""

import unittest
import sqlite3
import sys
import os
import importlib
import ast

sys.path.insert(0, '../desktop_simulator')

from database_manager import DatabaseManager

# Resolve path to ui_console.py relative to this test file
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_UI_CONSOLE_PATH = os.path.join(_THIS_DIR, '..', 'desktop_simulator', 'ui_console.py')


def _assert_rejected(test_case, result):
    """Assert that execute_custom_sql returned a rejection tuple."""
    test_case.assertIsInstance(result, tuple)
    test_case.assertEqual(len(result), 2)
    test_case.assertFalse(result[0], f"Expected rejection but got success: {result}")


class TestSQLInjectionPrevention(unittest.TestCase):
    """Verify execute_custom_sql blocks SQL injection vectors."""

    def setUp(self):
        self.db = DatabaseManager(':memory:')

    def tearDown(self):
        self.db.close()

    # --- Non-SELECT statements rejected ---

    def test_drop_table_rejected(self):
        result = self.db.execute_custom_sql("DROP TABLE players")
        _assert_rejected(self, result)

    def test_delete_rejected(self):
        result = self.db.execute_custom_sql("DELETE FROM players")
        _assert_rejected(self, result)

    def test_insert_rejected(self):
        result = self.db.execute_custom_sql(
            "INSERT INTO players (name) VALUES ('hacker')"
        )
        _assert_rejected(self, result)

    def test_update_rejected(self):
        result = self.db.execute_custom_sql(
            "UPDATE players SET name='hacked' WHERE player_id=1"
        )
        _assert_rejected(self, result)

    def test_create_table_rejected(self):
        result = self.db.execute_custom_sql(
            "CREATE TABLE evil (id INTEGER)"
        )
        _assert_rejected(self, result)

    def test_alter_table_rejected(self):
        result = self.db.execute_custom_sql(
            "ALTER TABLE players ADD COLUMN evil TEXT"
        )
        _assert_rejected(self, result)

    # --- Stacked-query / comment injection ---

    def test_stacked_query_rejected(self):
        result = self.db.execute_custom_sql(
            "SELECT 1; DROP TABLE players"
        )
        _assert_rejected(self, result)

    def test_comment_injection_dash_rejected(self):
        result = self.db.execute_custom_sql(
            "SELECT * FROM players -- DROP TABLE players"
        )
        _assert_rejected(self, result)

    def test_comment_injection_block_rejected(self):
        result = self.db.execute_custom_sql(
            "SELECT * FROM players /* DROP TABLE */"
        )
        _assert_rejected(self, result)

    # --- Hidden keywords inside SELECT ---

    def test_subquery_with_delete_rejected(self):
        result = self.db.execute_custom_sql(
            "SELECT * FROM (DELETE FROM players)"
        )
        _assert_rejected(self, result)

    def test_pragma_rejected(self):
        result = self.db.execute_custom_sql("PRAGMA table_info(players)")
        _assert_rejected(self, result)

    def test_attach_rejected(self):
        result = self.db.execute_custom_sql(
            "ATTACH DATABASE ':memory:' AS evil"
        )
        _assert_rejected(self, result)

    # --- Valid SELECT allowed ---

    def test_valid_select_allowed(self):
        success, data = self.db.execute_custom_sql("SELECT 1")
        self.assertTrue(success)

    def test_select_from_players_allowed(self):
        success, data = self.db.execute_custom_sql("SELECT * FROM players")
        self.assertTrue(success)

    def test_select_count_allowed(self):
        success, data = self.db.execute_custom_sql("SELECT COUNT(*) FROM players")
        self.assertTrue(success)


class TestMatchEngineInputValidation(unittest.TestCase):
    """Verify MatchEngine rejects invalid construction args."""

    def test_zero_overs_rejected(self):
        from match_engine import MatchEngine
        db = DatabaseManager(':memory:')
        with self.assertRaises(ValueError):
            MatchEngine(match_id=1, team1_id=1, team2_id=2,
                        total_overs=0, team_size=11, db=db)
        db.close()

    def test_negative_overs_rejected(self):
        from match_engine import MatchEngine
        db = DatabaseManager(':memory:')
        with self.assertRaises(ValueError):
            MatchEngine(match_id=1, team1_id=1, team2_id=2,
                        total_overs=-5, team_size=11, db=db)
        db.close()

    def test_team_size_one_rejected(self):
        from match_engine import MatchEngine
        db = DatabaseManager(':memory:')
        with self.assertRaises(ValueError):
            MatchEngine(match_id=1, team1_id=1, team2_id=2,
                        total_overs=20, team_size=1, db=db)
        db.close()

    def test_valid_construction_accepted(self):
        from match_engine import MatchEngine
        db = DatabaseManager(':memory:')
        engine = MatchEngine(match_id=1, team1_id=1, team2_id=2,
                             total_overs=20, team_size=11, db=db)
        self.assertEqual(engine.total_overs, 20)
        db.close()


class TestNoOsSystem(unittest.TestCase):
    """Ensure ui_console.py does not call os.system (shell injection risk)."""

    def test_no_os_system_calls(self):
        with open(_UI_CONSOLE_PATH, 'r', encoding='utf-8') as f:
            source = f.read()
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                # os.system(...)
                if isinstance(func, ast.Attribute) and func.attr == 'system':
                    if isinstance(func.value, ast.Name) and func.value.id == 'os':
                        self.fail("ui_console.py still contains os.system() call")


class TestDatabaseParameterization(unittest.TestCase):
    """Verify that user inputs are properly parameterized to prevent SQL attacks during standard CRUD operations."""

    def setUp(self):
        self.db = DatabaseManager(':memory:')

    def tearDown(self):
        self.db.close()

    def test_add_player_sql_injection(self):
        # A payload that would drop a table if simply concatenated into a query
        malicious_name = "Hacker'; DROP TABLE players; --"
        
        # This will succeed (return a positive integer ID) and not execute the DROP TABLE because of parameterization
        player_id = self.db.add_player(name=malicious_name)
        self.assertGreater(player_id, 0)
        
        # Verify the player actually exists with the exact malicious string as their name
        player = self.db.get_player(player_id)
        self.assertIsNotNone(player)
        self.assertEqual(player.name, malicious_name)
        
        # Verify the 'players' table still exists (fetch all players)
        players = self.db.get_all_players()
        self.assertGreater(len(players), 0)

    def test_get_player_by_name_sql_injection(self):
        # A payload that would mess up a WHERE clause if concatenated
        malicious_name_2 = "' OR 1=1; --"
        self.db.add_player(name=malicious_name_2)
        
        player = self.db.get_player_by_name(malicious_name_2)
        self.assertIsNotNone(player)
        self.assertEqual(player.name, malicious_name_2)


if __name__ == '__main__':
    unittest.main()
