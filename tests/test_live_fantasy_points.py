import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "desktop_simulator"))

from fantasy_engine import FantasyEngine
from models import BattingStats, BowlingStats


class StubDB:
    def __init__(self):
        self.players = {
            1: SimpleNamespace(name="Alice"),
            2: SimpleNamespace(name="Bob"),
        }

    def get_player(self, player_id):
        return self.players.get(player_id)


def test_live_fantasy_summary_is_sorted_by_total_points():
    engine = FantasyEngine(StubDB())

    batting_stats = {
        1: BattingStats(batting_stat_id=1, innings_id=10, player_id=1, runs_scored=40, balls_faced=20, boundaries=4, sixes=1),
        2: BattingStats(batting_stat_id=2, innings_id=10, player_id=2, runs_scored=10, balls_faced=12, boundaries=1, sixes=0, status="caught"),
    }
    bowling_stats = {
        2: BowlingStats(bowling_stat_id=1, innings_id=10, player_id=2, overs_bowled=2.0, runs_conceded=18, wickets_taken=1),
    }

    summary = engine.get_live_fantasy_summary(99, batting_stats, bowling_stats)

    assert summary[0][0] == "Alice"
    assert summary[0][1] > summary[1][1]
    assert summary[1][0] == "Bob"
