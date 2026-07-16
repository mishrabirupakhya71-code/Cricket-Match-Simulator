"""
Data models for the Cricket Match Simulator.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Player:
    """Player model."""
    player_id: int
    name: str
    batting_avg: float = 0.0
    strike_rate: float = 0.0
    runs: int = 0
    fours: int = 0
    sixes: int = 0
    twenties: int = 0
    fifties: int = 0
    bowling_avg: float = 0.0
    bowling_sr: float = 0.0
    wickets: int = 0
    economy_rate: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Ball:
    """Ball model for ball-by-ball tracking."""
    ball_id: int
    innings_id: int
    over_number: int
    ball_number: int
    striker_id: int
    bowler_id: int
    non_striker_id: int
    runs_off_bat: int = 0
    extras_type: str = 'none'  # 'wide', 'no_ball', 'leg_bye', 'bye', 'none'
    extra_runs: int = 0
    wicket_type: str = 'none'  # 'bowled', 'caught', 'lbw', 'run_out', 'stumped', 'none'
    fielder_id: Optional[int] = None
    is_dot_ball: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    
    def total_runs(self) -> int:
        """Return total runs (off bat + extras)."""
        return self.runs_off_bat + self.extra_runs


@dataclass
class BattingStats:
    """Batting statistics for a player in an innings."""
    batting_stat_id: int
    innings_id: int
    player_id: int
    runs_scored: int = 0
    balls_faced: int = 0
    boundaries: int = 0
    sixes: int = 0
    status: str = 'not_out'  # 'not_out', 'bowled', 'caught', 'lbw', 'run_out', 'stumped'
    
    def strike_rate(self) -> float:
        """Calculate strike rate."""
        if self.balls_faced == 0:
            return 0.0
        return (self.runs_scored / self.balls_faced) * 100
    
    def is_dismissed(self) -> bool:
        """Check if player is dismissed."""
        return self.status != 'not_out'


@dataclass
class BowlingStats:
    """Bowling statistics for a player in an innings."""
    bowling_stat_id: int
    innings_id: int
    player_id: int
    overs_bowled: float = 0.0
    runs_conceded: int = 0
    wickets_taken: int = 0
    dot_balls: int = 0
    wides: int = 0
    no_balls: int = 0
    
    def economy_rate(self) -> float:
        """Calculate economy rate."""
        if self.overs_bowled == 0:
            return 0.0
        return self.runs_conceded / self.overs_bowled
    
    def bowling_average(self) -> float:
        """Calculate bowling average."""
        if self.wickets_taken == 0:
            return float('inf')
        return self.runs_conceded / self.wickets_taken


@dataclass
class FantasyStats:
    """Fantasy statistics for a player in a match."""
    fantasy_stat_id: int
    player_id: int
    match_id: int
    total_points: float = 0.0
    run_points: float = 0.0
    boundary_points: float = 0.0
    six_points: float = 0.0
    wicket_points: float = 0.0
    dismissal_bonus: float = 0.0
    maiden_over_bonus: float = 0.0
    strike_rate_penalty: float = 0.0
    economy_penalty: float = 0.0
    
    def calculate_total(self) -> float:
        """Calculate total fantasy points."""
        self.total_points = (
            self.run_points +
            self.boundary_points +
            self.six_points +
            self.wicket_points +
            self.dismissal_bonus +
            self.maiden_over_bonus +
            self.strike_rate_penalty +
            self.economy_penalty
        )
        return self.total_points


@dataclass
class Match:
    """Match model."""
    match_id: int
    match_name: str
    total_overs: int
    team_size: int
    toss_winner_id: int
    toss_decision: str  # 'bat' or 'bowl'
    match_status: str = 'ongoing'  # 'ongoing', 'completed', 'paused'
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Team:
    """Team model."""
    team_id: int
    match_id: int
    team_name: str
    batting_order: int  # 1 or 2
    players: List[Player] = field(default_factory=list)


@dataclass
class Innings:
    """Innings model."""
    innings_id: int
    match_id: int
    batting_team_id: int
    bowling_team_id: int
    innings_number: int
    total_runs: int = 0
    total_wickets: int = 0
    overs_bowled: float = 0.0
    status: str = 'ongoing'  # 'ongoing', 'completed'
    balls: List[Ball] = field(default_factory=list)


@dataclass
class Scorecard:
    """Real-time scorecard display model."""
    batting_team_name: str
    bowling_team_name: str
    current_runs: int
    current_wickets: int
    overs_played: float
    striker_name: str
    striker_runs: int
    striker_balls: int
    non_striker_name: str
    non_striker_runs: int
    non_striker_balls: int
    bowler_name: str
    bowler_runs: int
    bowler_wickets: int
    last_five_balls: List[str]  # Last 5 balls representation
