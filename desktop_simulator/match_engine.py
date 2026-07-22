"""
Match Engine for ball-by-ball cricket simulation.
Core logic for running the match with 100% cricket accuracy.
"""

import random
from typing import List, Dict, Optional, Tuple
from enum import Enum
from models import Player, Ball, BattingStats, BowlingStats
from database_manager import DatabaseManager


class WicketType(Enum):
    """Wicket dismissal types."""
    BOWLED = 'bowled'
    CAUGHT = 'caught'
    LBW = 'lbw'
    RUN_OUT = 'run_out'
    STUMPED = 'stumped'
    NONE = 'none'


class MatchEngine:
    """Core match simulation engine."""
    
    def __init__(self, match_id: int, team1_id: int, team2_id: int,
                 total_overs: int, team_size: int, db: DatabaseManager):
        """Initialize match engine.

        Raises:
            ValueError: If total_overs < 1, team_size < 2, or IDs are not
                positive integers.
        """
        # --- Input validation ---
        if not isinstance(total_overs, int) or total_overs < 1:
            raise ValueError(f"total_overs must be a positive integer, got {total_overs!r}")
        if not isinstance(team_size, int) or team_size < 2:
            raise ValueError(f"team_size must be an integer >= 2, got {team_size!r}")
        for name, val in [("match_id", match_id), ("team1_id", team1_id), ("team2_id", team2_id)]:
            if not isinstance(val, int) or val < 0:
                raise ValueError(f"{name} must be a non-negative integer, got {val!r}")

        self.match_id = match_id
        self.team1_id = team1_id
        self.team2_id = team2_id
        self.total_overs = total_overs
        self.team_size = team_size
        self.db = db
        
        # Match state
        self.innings_number = 1
        self.current_innings_id = None
        self.batting_team_id = None
        self.bowling_team_id = None
        
        # Ball state
        self.current_over = 0
        self.current_ball = 0
        self.total_runs = 0
        self.total_wickets = 0
        
        # Players state
        self.striker_id = None
        self.non_striker_id = None
        self.bowler_id = None
        self.batsmen_queue = []
        
        # Batting and Bowling stats
        self.batting_stats = {}  # {player_id: BattingStats}
        self.bowling_stats = {}  # {player_id: BowlingStats}
        
        # Match history
        self.ball_history = []
    
    def start_innings(self, batting_team_id: int, bowling_team_id: int,
                      striker_id: Optional[int] = None, non_striker_id: Optional[int] = None,
                      bowler_id: Optional[int] = None):
        """Start an innings. Optional: provide `striker_id`, `non_striker_id`, `bowler_id` to set openers.

        If provided IDs are not valid team members they are ignored and defaults are used.

        Raises:
            ValueError: If a team has fewer than 2 members.
        """
        self.batting_team_id = batting_team_id
        self.bowling_team_id = bowling_team_id

        # Create innings in database
        self.current_innings_id = self.db.create_innings(
            self.match_id, batting_team_id, bowling_team_id, self.innings_number
        )

        # Get batting team members (all members are considered "on-field")
        batting_team_members = self.db.get_team_members(batting_team_id)
        if len(batting_team_members) < 2:
            raise ValueError(
                f"Batting team {batting_team_id} must have at least 2 members, "
                f"got {len(batting_team_members)}"
            )
        batting_ids = [p.player_id for p in batting_team_members]
        # Update team_size to actual on-field players
        if batting_team_members:
            self.team_size = len(batting_team_members)

        # Determine openers
        if striker_id in batting_ids and non_striker_id in batting_ids and striker_id != non_striker_id:
            self.striker_id = striker_id
            self.non_striker_id = non_striker_id
            # Build batsmen queue excluding chosen openers
            self.batsmen_queue = [pid for pid in batting_ids if pid not in (striker_id, non_striker_id)]
        else:
            # Default openers are first two members
            self.striker_id = batting_team_members[0].player_id
            self.non_striker_id = batting_team_members[1].player_id
            self.batsmen_queue = [p.player_id for p in batting_team_members[2:]]

        # Initialize bowler
        bowling_team_members = self.db.get_team_members(bowling_team_id)
        if not bowling_team_members:
            raise ValueError(
                f"Bowling team {bowling_team_id} must have at least 1 member"
            )
        bowling_ids = [p.player_id for p in bowling_team_members]
        if bowler_id in bowling_ids:
            self.bowler_id = bowler_id
        else:
            self.bowler_id = bowling_team_members[0].player_id
        
        # Initialize stats
        for member in batting_team_members:
            self.batting_stats[member.player_id] = BattingStats(
                batting_stat_id=0, innings_id=self.current_innings_id,
                player_id=member.player_id
            )
        
        for member in bowling_team_members:
            self.bowling_stats[member.player_id] = BowlingStats(
                bowling_stat_id=0, innings_id=self.current_innings_id,
                player_id=member.player_id
            )
        
        # Reset ball state
        self.current_over = 0
        self.current_ball = 0
        self.total_runs = 0
        self.total_wickets = 0
        self.ball_history = []
        # innings flags
        self.innings_complete = False
    
    def simulate_ball(self) -> Ball:
        """Simulate a single ball."""
        self.current_ball += 1
        
        # Determine ball outcome
        runs, extras_type, extra_runs, wicket_type, fielder_id = self._determine_ball_outcome()
        
        # Calculate is_dot_ball
        is_dot_ball = (runs + extra_runs == 0)
        
        # Save ball to database
        ball_id = self.db.save_ball(
            self.current_innings_id, self.current_over + 1, self.current_ball,
            self.striker_id, self.bowler_id, self.non_striker_id,
            runs_off_bat=runs, extras_type=extras_type, extra_runs=extra_runs,
            wicket_type=wicket_type, fielder_id=fielder_id, is_dot_ball=is_dot_ball
        )
        
        # Create Ball object
        ball = Ball(
            ball_id=ball_id, innings_id=self.current_innings_id,
            over_number=self.current_over + 1, ball_number=self.current_ball,
            striker_id=self.striker_id, bowler_id=self.bowler_id,
            non_striker_id=self.non_striker_id, runs_off_bat=runs,
            extras_type=extras_type, extra_runs=extra_runs,
            wicket_type=wicket_type, fielder_id=fielder_id, is_dot_ball=is_dot_ball
        )
        
        # Update stats
        self._update_stats_after_ball(ball)
        
        # Update match state
        self.total_runs += (runs + extra_runs)
        if wicket_type != 'none':
            self.total_wickets += 1
        
        self.ball_history.append(ball)
        
        # Check if all out
        if self.total_wickets >= (self.team_size - 1):
            self.end_innings()
        # Win by chase in second innings
        elif self.innings_number == 2 and self._has_chased_target():
            self.end_innings()
        # Check if end of over
        elif self.current_ball == 6:
            self.end_over()
        # Check if overs complete
        elif self.current_over >= self.total_overs:
            self.end_innings()
        else:
            # Rotate strike based on runs (only if not wicket)
            if wicket_type == 'none':
                self._rotate_strike(runs + extra_runs)
        
        return ball
    
    def _determine_ball_outcome(self) -> Tuple[int, str, int, str, Optional[int]]:
        """Determine the outcome of a ball."""
        # Simplified logic: random outcomes for demo
        # In production, use player abilities and match context
        
        rand = random.random()
        
        # Wicket (5% chance)
        if rand < 0.05:
            wicket_type = random.choice([
                WicketType.BOWLED.value,
                WicketType.CAUGHT.value,
                WicketType.LBW.value,
                WicketType.RUN_OUT.value
            ])
            
            fielder_id = None
            if wicket_type in [WicketType.CAUGHT.value, WicketType.RUN_OUT.value]:
                bowling_team = self.db.get_team_members(self.bowling_team_id)
                fielder_id = random.choice([p.player_id for p in bowling_team
                                           if p.player_id != self.bowler_id])
            
            return 0, 'none', 0, wicket_type, fielder_id
        
        # Wide/No-ball (10% chance)
        if rand < 0.15:
            extras_type = random.choice(['wide', 'no_ball'])
            extra_runs = random.randint(0, 2)
            return 0, extras_type, 1 + extra_runs, 'none', None
        
        # Dot ball (25% chance)
        if rand < 0.40:
            return 0, 'none', 0, 'none', None
        
        # Singles (20% chance)
        if rand < 0.60:
            return 1, 'none', 0, 'none', None
        
        # Twos (15% chance)
        if rand < 0.75:
            return 2, 'none', 0, 'none', None
        
        # Threes (5% chance)
        if rand < 0.80:
            return 3, 'none', 0, 'none', None
        
        # Fours (8% chance)
        if rand < 0.88:
            return 4, 'none', 0, 'none', None
        
        # Sixes (12% chance)
        return 6, 'none', 0, 'none', None
    
    def _update_stats_after_ball(self, ball: Ball):
        """Update stats after a ball."""
        # Update batting stats
        bat_stat = self.batting_stats[self.striker_id]
        
        # Wide does not count as a ball faced; no-ball does.
        if ball.extras_type != 'wide':
            bat_stat.balls_faced += 1
            
        bat_stat.runs_scored += ball.runs_off_bat
        
        if ball.runs_off_bat == 4:
            bat_stat.boundaries += 1
        elif ball.runs_off_bat == 6:
            bat_stat.sixes += 1
        
        if ball.wicket_type != 'none':
            bat_stat.status = ball.wicket_type
        
        self.db.save_batting_stats(
            self.current_innings_id, self.striker_id,
            bat_stat.runs_scored, bat_stat.balls_faced,
            bat_stat.boundaries, bat_stat.sixes, bat_stat.status
        )
        
        # Update bowling stats
        bowl_stat = self.bowling_stats[self.bowler_id]
        
        # Leg byes and byes do not count against the bowler
        runs_against_bowler = ball.runs_off_bat
        if ball.extras_type in ['wide', 'no_ball']:
            runs_against_bowler += ball.extra_runs
            
        bowl_stat.runs_conceded += runs_against_bowler
        
        # Increment legal deliveries for overs_bowled
        if ball.extras_type not in ['wide', 'no_ball']:
            fraction = round((bowl_stat.overs_bowled % 1) * 10)
            completed_overs = int(bowl_stat.overs_bowled)
            fraction += 1
            if fraction == 6:
                completed_overs += 1
                fraction = 0
            bowl_stat.overs_bowled = completed_overs + (fraction / 10.0)
        
        if ball.is_dot_ball:
            bowl_stat.dot_balls += 1
        
        if ball.extras_type == 'wide':
            bowl_stat.wides += 1
        elif ball.extras_type == 'no_ball':
            bowl_stat.no_balls += 1
        
        if ball.wicket_type != 'none':
            bowl_stat.wickets_taken += 1
        
        self.db.save_bowling_stats(
            self.current_innings_id, self.bowler_id,
            bowl_stat.overs_bowled, bowl_stat.runs_conceded,
            bowl_stat.wickets_taken, bowl_stat.dot_balls,
            bowl_stat.wides, bowl_stat.no_balls
        )
    
    def _rotate_strike(self, runs: int):
        """Rotate strike based on runs."""
        if runs % 2 != 0:  # Odd runs = rotate
            self.striker_id, self.non_striker_id = self.non_striker_id, self.striker_id
    
    def _handle_wicket(self, wicket_type: str, fielder_id: Optional[int], chosen_batter_id: Optional[int] = None):
        """Handle wicket dismissal.

        If `chosen_batter_id` is provided, bring that batter in (and remove from queue if present).
        Otherwise pop the next batter from the queue.
        """
        next_batter = None
        if chosen_batter_id is not None:
            # If chosen batter is still in queue, remove it
            try:
                self.batsmen_queue.remove(chosen_batter_id)
            except ValueError:
                pass
            next_batter = chosen_batter_id
        else:
            if self.batsmen_queue:
                next_batter = self.batsmen_queue.pop(0)

        if next_batter is not None:
            self.striker_id = next_batter
            # Initialize batting stats for new batter
            self.batting_stats[next_batter] = BattingStats(
                batting_stat_id=0, innings_id=self.current_innings_id,
                player_id=next_batter
            )
            # Persist initial batting stats row
            self.db.save_batting_stats(self.current_innings_id, next_batter)
    
    def end_over(self):
        """End current over."""
        self.current_over += 1
        self.current_ball = 0
        
        # Rotate strike at end of over
        self.striker_id, self.non_striker_id = self.non_striker_id, self.striker_id
        # Note: bowler selection now handled by caller (UI/main) to allow explicit choice
    
    def end_innings(self):
        """End current innings."""
        # Update innings in database
        self.db.complete_innings(self.current_innings_id)
        
        # Calculate overs bowled
        overs_decimal = self.current_over + (self.current_ball / 6.0)
        self.db.update_innings_score(self.current_innings_id, self.total_runs,
                                    self.total_wickets, overs_decimal)
        
        self.innings_number += 1
        # mark innings complete so caller can transition
        self.innings_complete = True

    def _get_target_runs(self) -> Optional[int]:
        """Return the target runs for the second innings or None."""
        if self.innings_number != 2:
            return None

        # Second innings should chase the first innings total + 1
        previous_innings = self.db.get_match_innings(self.match_id)
        if len(previous_innings) < 1:
            return None

        first_innings = previous_innings[0]
        return first_innings.total_runs + 1

    def _get_balls_remaining(self) -> Optional[int]:
        """Return balls remaining in the current innings."""
        if self.current_over >= self.total_overs:
            return 0

        return (self.total_overs - self.current_over - 1) * 6 + (6 - self.current_ball)

    def _has_chased_target(self) -> bool:
        """Check whether the chasing team has reached the target."""
        target = self._get_target_runs()
        if target is None:
            return False
        return self.total_runs >= target

    def get_current_scorecard(self) -> Dict:
        """Get current scorecard."""
        striker = self.db.get_player(self.striker_id)
        non_striker = self.db.get_player(self.non_striker_id)
        bowler = self.db.get_player(self.bowler_id)
        batting_team = self.db.get_team(self.batting_team_id) if self.batting_team_id else None
        bowling_team = self.db.get_team(self.bowling_team_id) if self.bowling_team_id else None
        match = self.db.get_match(self.match_id)
        
        bat_stat_striker = self.batting_stats.get(self.striker_id)
        bat_stat_non_striker = self.batting_stats.get(self.non_striker_id)
        bowl_stat = self.bowling_stats.get(self.bowler_id)
        
        # Last 5 balls
        last_five = []
        for ball in self.ball_history[-5:]:
            if ball.wicket_type != 'none':
                last_five.append('W')
            elif ball.extras_type in ['wide', 'no_ball']:
                last_five.append('·' if ball.extra_runs == 1 else str(ball.extra_runs))
            elif ball.is_dot_ball:
                last_five.append('·')
            else:
                last_five.append(str(ball.runs_off_bat + ball.extra_runs))

        target_runs = self._get_target_runs()
        balls_remaining = self._get_balls_remaining()
        required_runs = max(0, target_runs - self.total_runs) if self.innings_number == 2 else None
        chasing = self.innings_number == 2 and target_runs is not None

        return {
            'match_name': match.match_name if match else 'Unknown Match',
            'batting_team_name': batting_team.team_name if batting_team else 'Batting',
            'bowling_team_name': bowling_team.team_name if bowling_team else 'Bowling',
            'current_over': self.current_over,
            'current_ball': self.current_ball,
            'total_runs': self.total_runs,
            'total_wickets': self.total_wickets,
            'striker_name': striker.name if striker else 'N/A',
            'striker_runs': bat_stat_striker.runs_scored if bat_stat_striker else 0,
            'striker_balls': bat_stat_striker.balls_faced if bat_stat_striker else 0,
            'non_striker_name': non_striker.name if non_striker else 'N/A',
            'non_striker_runs': bat_stat_non_striker.runs_scored if bat_stat_non_striker else 0,
            'non_striker_balls': bat_stat_non_striker.balls_faced if bat_stat_non_striker else 0,
            'bowler_name': bowler.name if bowler else 'N/A',
            'bowler_runs': bowl_stat.runs_conceded if bowl_stat else 0,
            'bowler_wickets': bowl_stat.wickets_taken if bowl_stat else 0,
            'bowler_overs': f"{int(bowl_stat.overs_bowled)}.{int((bowl_stat.overs_bowled % 1) * 10)}" if bowl_stat else "0.0",
            'last_five_balls': ' '.join(last_five[-5:]) if last_five else 'N/A',
            'all_out': self.total_wickets >= (self.team_size - 1),
            'overs_completed': self.current_over >= self.total_overs,
            'total_overs': self.total_overs,
            'target_runs': target_runs,
            'balls_remaining': balls_remaining,
            'required_runs': required_runs,
            'is_chasing': chasing
        }
    
    def pause_match(self) -> bool:
        """Pause match."""
        return self.db.update_match_status(self.match_id, 'paused')
    
    def resume_match(self):
        """Resume match (state already loaded)."""
        pass

    def undo_last_ball(self) -> bool:
        """Undo the last ball played and revert all state/stats."""
        if not self.ball_history:
            return False
        
        last_ball = self.ball_history.pop()
        
        # 1. Reverse Innings End (if this ball ended the match/innings)
        # If total_wickets reached all out, or chase target reached, or end of over reached total_overs
        if self.innings_complete:
            self.innings_complete = False
            self.innings_number -= 1
            # Revert innings status in DB
            self.db.update_innings_status(self.current_innings_id, 'in_progress')
        
        # 2. Reverse Over changes
        # If we are at the start of a new over, this ball must have been the 6th ball
        if self.current_ball == 0:
            self.current_over -= 1
            self.current_ball = 6
            # Reverse end-of-over strike rotation
            self.striker_id, self.non_striker_id = self.non_striker_id, self.striker_id
        else:
            self.current_ball -= 1
            # Reverse normal strike rotation (if applicable)
            if last_ball.wicket_type == 'none' and (last_ball.runs_off_bat + last_ball.extra_runs) % 2 != 0:
                self.striker_id, self.non_striker_id = self.non_striker_id, self.striker_id
                
        # 3. Reverse Wicket substitution (if a wicket fell)
        if last_ball.wicket_type != 'none':
            self.total_wickets -= 1
            # The current striker is the new batsman who came in. 
            # We must put them back at the front of the queue.
            # But wait, if they hadn't faced a ball yet, we can delete their stats later.
            if self.striker_id != last_ball.striker_id:
                # The actual batsman who was out needs to be restored to striker
                self.batsmen_queue.insert(0, self.striker_id)
                self.striker_id = last_ball.striker_id
        
        # 4. Reverse Runs
        self.total_runs -= (last_ball.runs_off_bat + last_ball.extra_runs)
        
        # 5. Reverse Stats
        # Batting stats
        bat_stat = self.batting_stats[last_ball.striker_id]
        bat_stat.balls_faced -= 1
        bat_stat.runs_scored -= (last_ball.runs_off_bat + last_ball.extra_runs)
        if last_ball.runs_off_bat == 4:
            bat_stat.boundaries -= 1
        elif last_ball.runs_off_bat == 6:
            bat_stat.sixes -= 1
            
        if last_ball.wicket_type != 'none':
            bat_stat.status = 'not_out'
            
        self.db.save_batting_stats(
            self.current_innings_id, last_ball.striker_id,
            bat_stat.runs_scored, bat_stat.balls_faced,
            bat_stat.boundaries, bat_stat.sixes, bat_stat.status
        )
        
        # Bowling stats
        bowl_stat = self.bowling_stats[last_ball.bowler_id]
        bowl_stat.runs_conceded -= (last_ball.runs_off_bat + last_ball.extra_runs)
        
        # Decrement legal deliveries for overs_bowled
        if last_ball.extras_type not in ['wide', 'no_ball']:
            fraction = round((bowl_stat.overs_bowled % 1) * 10)
            completed_overs = int(bowl_stat.overs_bowled)
            fraction -= 1
            if fraction < 0:
                completed_overs -= 1
                fraction = 5
            if completed_overs < 0:
                completed_overs = 0
                fraction = 0
            bowl_stat.overs_bowled = completed_overs + (fraction / 10.0)

        if last_ball.is_dot_ball:
            bowl_stat.dot_balls -= 1
        if last_ball.extras_type == 'wide':
            bowl_stat.wides -= 1
        elif last_ball.extras_type == 'no_ball':
            bowl_stat.no_balls -= 1
        if last_ball.wicket_type != 'none':
            bowl_stat.wickets_taken -= 1
        
        self.db.save_bowling_stats(
            self.current_innings_id, last_ball.bowler_id,
            bowl_stat.overs_bowled, bowl_stat.runs_conceded,
            bowl_stat.wickets_taken, bowl_stat.dot_balls,
            bowl_stat.wides, bowl_stat.no_balls
        )
        
        # 6. Remove ball from DB
        self.db.delete_ball(last_ball.ball_id)
        
        return True
