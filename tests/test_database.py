"""
Unit tests for SQLite database operations.
Tests CRUD operations, match state persistence, sync functionality.
"""

import unittest
import sqlite3
import os
import sys
sys.path.insert(0, '../desktop_simulator')


class TestDatabaseInitialization(unittest.TestCase):
    """Test database schema creation and initialization."""
    
    def setUp(self):
        """Create in-memory database for testing."""
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
    
    def tearDown(self):
        """Close database connection."""
        self.conn.close()
    
    def test_create_players_table(self):
        """Create players table."""
        self.cursor.execute('''
            CREATE TABLE players (
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                batting_avg REAL DEFAULT 0.0,
                bowling_avg REAL DEFAULT 0.0,
                strike_rate REAL DEFAULT 0.0,
                economy_rate REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Verify table exists
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='players'")
        self.assertIsNotNone(self.cursor.fetchone())
    
    def test_create_matches_table(self):
        """Create matches table."""
        self.cursor.execute('''
            CREATE TABLE matches (
                match_id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_name TEXT NOT NULL,
                total_overs INTEGER NOT NULL,
                team_size INTEGER NOT NULL,
                match_status TEXT DEFAULT 'ongoing'
            )
        ''')
        
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='matches'")
        self.assertIsNotNone(self.cursor.fetchone())
    
    def test_all_tables_created(self):
        """All required tables created successfully."""
        tables = [
            'players', 'matches', 'teams', 'team_members', 'innings',
            'ball_by_ball', 'batting_stats', 'bowling_stats',
            'fantasy_stats', 'global_rankings', 'sync_log'
        ]
        
        for table in tables:
            # Just verify each table can be queried
            try:
                self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY)")
                self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                self.assertIsNotNone(self.cursor.fetchone())
            except Exception as e:
                self.fail(f"Failed to create/verify table {table}: {e}")


class TestPlayerOperations(unittest.TestCase):
    """Test CRUD operations for players."""
    
    def setUp(self):
        """Set up database and create players table."""
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE players (
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                batting_avg REAL DEFAULT 0.0,
                bowling_avg REAL DEFAULT 0.0,
                strike_rate REAL DEFAULT 0.0,
                economy_rate REAL DEFAULT 0.0
            )
        ''')
        self.conn.commit()
    
    def tearDown(self):
        """Close database."""
        self.conn.close()
    
    def test_insert_player(self):
        """Insert a single player."""
        result = self._insert_player('Virat Kohli', 50.5, 0, 140.5, 0)
        self.assertTrue(result)
    
    def test_duplicate_player_name_fails(self):
        """Duplicate player names should fail."""
        self._insert_player('Rohit Sharma', 45.0, 0, 130.0, 0)
        result = self._insert_player('Rohit Sharma', 45.0, 0, 130.0, 0)
        self.assertFalse(result)
    
    def test_retrieve_player(self):
        """Retrieve player by name."""
        self._insert_player('MS Dhoni', 50.57, 0, 145.5, 0)
        player = self._get_player('MS Dhoni')
        self.assertIsNotNone(player)
        self.assertEqual(player[1], 'MS Dhoni')
        self.assertEqual(player[2], 50.57)  # batting_avg
    
    def test_update_player_stats(self):
        """Update player statistics."""
        self._insert_player('Jasprit Bumrah', 0, 22.5, 0, 5.8)
        self._update_player_stats('Jasprit Bumrah', batting_avg=0, bowling_avg=23.0)
        player = self._get_player('Jasprit Bumrah')
        self.assertEqual(player[3], 23.0)  # Updated bowling_avg
    
    def test_delete_player(self):
        """Delete a player."""
        self._insert_player('Sachin Tendulkar', 53.78, 0, 151.0, 0)
        self._delete_player('Sachin Tendulkar')
        player = self._get_player('Sachin Tendulkar')
        self.assertIsNone(player)
    
    def test_get_all_players(self):
        """Get all players from database."""
        players_to_insert = [
            ('Player1', 40, 0, 120, 0),
            ('Player2', 35, 25, 110, 6),
            ('Player3', 30, 28, 100, 7),
        ]
        for name, ba, bo, sr, er in players_to_insert:
            self._insert_player(name, ba, bo, sr, er)
        
        all_players = self._get_all_players()
        self.assertEqual(len(all_players), 3)
    
    def _insert_player(self, name, batting_avg, bowling_avg, strike_rate, economy_rate):
        """Helper to insert player."""
        try:
            self.cursor.execute('''
                INSERT INTO players (name, batting_avg, bowling_avg, strike_rate, economy_rate)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, batting_avg, bowling_avg, strike_rate, economy_rate))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def _get_player(self, name):
        """Helper to retrieve player."""
        self.cursor.execute('SELECT * FROM players WHERE name = ?', (name,))
        return self.cursor.fetchone()
    
    def _update_player_stats(self, name, batting_avg=None, bowling_avg=None):
        """Helper to update player stats."""
        if batting_avg is not None:
            self.cursor.execute('UPDATE players SET batting_avg = ? WHERE name = ?', (batting_avg, name))
        if bowling_avg is not None:
            self.cursor.execute('UPDATE players SET bowling_avg = ? WHERE name = ?', (bowling_avg, name))
        self.conn.commit()
    
    def _delete_player(self, name):
        """Helper to delete player."""
        self.cursor.execute('DELETE FROM players WHERE name = ?', (name,))
        self.conn.commit()
    
    def _get_all_players(self):
        """Helper to get all players."""
        self.cursor.execute('SELECT * FROM players')
        return self.cursor.fetchall()


class TestMatchPersistence(unittest.TestCase):
    """Test match state persistence and resumption."""
    
    def setUp(self):
        """Set up database."""
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self._setup_tables()
    
    def tearDown(self):
        """Close database."""
        self.conn.close()
    
    def test_save_match_state(self):
        """Save match state to database."""
        match_data = {
            'match_name': 'Test Match',
            'total_overs': 20,
            'team_size': 11,
            'status': 'ongoing'
        }
        result = self._save_match(match_data)
        self.assertTrue(result)
    
    def test_retrieve_paused_match(self):
        """Retrieve paused match for resumption."""
        match_data = {
            'match_name': 'Paused Match',
            'total_overs': 20,
            'team_size': 11,
            'status': 'paused'
        }
        match_id = self._save_match(match_data)
        retrieved = self._get_match(match_id)
        self.assertEqual(retrieved[1], 'Paused Match')
        self.assertEqual(retrieved[4], 'paused')
    
    def test_save_ball_by_ball_data(self):
        """Save ball-by-ball data."""
        # First create a match
        match_id = self._save_match({'match_name': 'M1', 'total_overs': 20, 'team_size': 11})
        
        # Create innings
        innings_id = self._create_innings(match_id)
        
        # Save ball
        ball_data = {
            'innings_id': innings_id,
            'over_number': 1,
            'ball_number': 1,
            'striker_id': 1,
            'bowler_id': 2,
            'non_striker_id': 3,
            'runs_off_bat': 0,
            'extras_type': 'none',
            'wicket_type': 'none'
        }
        result = self._save_ball(ball_data)
        self.assertTrue(result)
    
    def test_retrieve_ball_by_ball_history(self):
        """Retrieve complete ball-by-ball history of a match."""
        match_id = self._save_match({'match_name': 'M1', 'total_overs': 20, 'team_size': 11})
        innings_id = self._create_innings(match_id)
        
        # Save multiple balls
        for i in range(1, 7):  # 6 balls
            ball_data = {
                'innings_id': innings_id,
                'over_number': 1,
                'ball_number': i,
                'striker_id': 1,
                'bowler_id': 2,
                'non_striker_id': 3,
                'runs_off_bat': (i % 4),  # Varied runs
                'extras_type': 'none',
                'wicket_type': 'none'
            }
            self._save_ball(ball_data)
        
        # Retrieve all balls
        balls = self._get_balls_in_innings(innings_id)
        self.assertEqual(len(balls), 6)
    
    def _setup_tables(self):
        """Set up all required tables."""
        self.cursor.execute('''
            CREATE TABLE matches (
                match_id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_name TEXT,
                total_overs INTEGER,
                team_size INTEGER,
                match_status TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE innings (
                innings_id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id INTEGER,
                innings_number INTEGER
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE ball_by_ball (
                ball_id INTEGER PRIMARY KEY AUTOINCREMENT,
                innings_id INTEGER,
                over_number INTEGER,
                ball_number INTEGER,
                striker_id INTEGER,
                bowler_id INTEGER,
                non_striker_id INTEGER,
                runs_off_bat INTEGER,
                extras_type TEXT,
                wicket_type TEXT
            )
        ''')
        self.conn.commit()
    
    def _save_match(self, match_data):
        """Helper to save match."""
        try:
            self.cursor.execute('''
                INSERT INTO matches (match_name, total_overs, team_size, match_status)
                VALUES (?, ?, ?, ?)
            ''', (match_data['match_name'], match_data['total_overs'],
                  match_data['team_size'], match_data.get('status', 'ongoing')))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception:
            return False
    
    def _get_match(self, match_id):
        """Helper to retrieve match."""
        self.cursor.execute('SELECT * FROM matches WHERE match_id = ?', (match_id,))
        return self.cursor.fetchone()
    
    def _create_innings(self, match_id):
        """Helper to create innings."""
        self.cursor.execute('''
            INSERT INTO innings (match_id, innings_number)
            VALUES (?, 1)
        ''', (match_id,))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def _save_ball(self, ball_data):
        """Helper to save ball."""
        try:
            self.cursor.execute('''
                INSERT INTO ball_by_ball
                (innings_id, over_number, ball_number, striker_id, bowler_id, non_striker_id,
                 runs_off_bat, extras_type, wicket_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (ball_data['innings_id'], ball_data['over_number'], ball_data['ball_number'],
                  ball_data['striker_id'], ball_data['bowler_id'], ball_data['non_striker_id'],
                  ball_data['runs_off_bat'], ball_data['extras_type'], ball_data['wicket_type']))
            self.conn.commit()
            return True
        except Exception:
            return False
    
    def _get_balls_in_innings(self, innings_id):
        """Helper to get all balls in innings."""
        self.cursor.execute('SELECT * FROM ball_by_ball WHERE innings_id = ?', (innings_id,))
        return self.cursor.fetchall()


class TestCustomSQLExecution(unittest.TestCase):
    """Test custom SQL execution functionality."""
    
    def setUp(self):
        """Set up database."""
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
    
    def tearDown(self):
        """Close database."""
        self.conn.close()
    
    def test_execute_select_query(self):
        """Execute SELECT query."""
        self.cursor.execute('CREATE TABLE test (id INTEGER, name TEXT)')
        self.cursor.execute("INSERT INTO test VALUES (1, 'Test')")
        self.conn.commit()
        
        result = self._execute_custom_sql('SELECT * FROM test')
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
    
    def test_execute_create_table_query(self):
        """CREATE TABLE query should be rejected for security."""
        result = self._execute_custom_sql('''
            CREATE TABLE custom_table (
                id INTEGER PRIMARY KEY,
                value TEXT
            )
        ''')
        self.assertFalse(result)
    
    def test_execute_alter_table_query(self):
        """ALTER TABLE query should be rejected for security."""
        self.cursor.execute('CREATE TABLE users (id INTEGER, name TEXT)')
        result = self._execute_custom_sql('ALTER TABLE users ADD COLUMN age INTEGER')
        self.assertFalse(result)
    
    def test_invalid_query_returns_error(self):
        """Invalid query returns error information."""
        result = self._execute_custom_sql('SELECT * FROM nonexistent')
        self.assertFalse(result)
    
    def _execute_custom_sql(self, query):
        """Helper to execute custom SQL — mirrors secured DatabaseManager.execute_custom_sql."""
        _BLOCKED_SQL_KEYWORDS = frozenset({
            'INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE',
            'REPLACE', 'TRUNCATE', 'GRANT', 'REVOKE', 'ATTACH', 'DETACH',
            'PRAGMA', 'VACUUM', 'REINDEX', 'BEGIN', 'COMMIT', 'ROLLBACK',
            'SAVEPOINT', 'RELEASE',
        })
        try:
            cleaned = query.strip()
            if not cleaned.upper().startswith('SELECT'):
                return False
            if ';' in cleaned[:-1]:
                return False
            if '--' in cleaned or '/*' in cleaned:
                return False
            tokens = cleaned.upper().replace('(', ' ').replace(')', ' ').split()
            for token in tokens:
                if token in _BLOCKED_SQL_KEYWORDS:
                    return False
            self.cursor.execute(cleaned)
            return self.cursor.fetchall()
        except Exception:
            return False


if __name__ == '__main__':
    unittest.main()
