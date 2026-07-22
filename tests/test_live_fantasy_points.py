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
            3: SimpleNamespace(name="Charlie"),
            4: SimpleNamespace(name="David"),
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


def test_fantasy_strike_rate_penalty():
    engine = FantasyEngine(StubDB())

    # Player 1 faces 10 balls, gets 5 runs -> strike rate is 50.0 (< 60.0). Deficit = 10 -> -1 penalty.
    stats_with_penalty = BattingStats(batting_stat_id=1, innings_id=10, player_id=1, runs_scored=5, balls_faced=10, boundaries=0, sixes=0)
    pts = engine.calculate_batting_points(stats_with_penalty)
    assert pts['strike_rate_penalty'] == -1.0

    # Player 2 faces 9 balls, gets 4 runs -> strike rate is 44.4 (< 60.0), but balls faced < 10 so no penalty.
    stats_no_penalty = BattingStats(batting_stat_id=2, innings_id=10, player_id=2, runs_scored=4, balls_faced=9, boundaries=0, sixes=0)
    pts = engine.calculate_batting_points(stats_no_penalty)
    assert pts['strike_rate_penalty'] == 0.0


def test_fantasy_economy_penalty():
    engine = FantasyEngine(StubDB())

    # Bowler bowls 1.0 over, concedes 9 runs -> economy is 9.0 (> 8.0). Excess = 1.0 -> -1 penalty.
    stats_with_penalty = BowlingStats(bowling_stat_id=1, innings_id=10, player_id=1, overs_bowled=1.0, runs_conceded=9, wickets_taken=0)
    pts = engine.calculate_bowling_points(stats_with_penalty)
    assert pts['economy_penalty'] == -1.0

    # Bowler bowls 0.5 overs, concedes 6 runs -> economy is 12.0 (> 8.0), but overs bowled < 1.0 so no penalty.
    stats_no_penalty = BowlingStats(bowling_stat_id=2, innings_id=10, player_id=2, overs_bowled=0.5, runs_conceded=6, wickets_taken=0)
    pts = engine.calculate_bowling_points(stats_no_penalty)
    assert pts['economy_penalty'] == 0.0

