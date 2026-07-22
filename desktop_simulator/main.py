"""
Cricket Match Simulator - Main Entry Point.
Console-based application for cricket match simulation with fantasy points.
Implements all 16 fundamentals for professional cricket scoreboard system.
"""

import sys
from datetime import datetime
from typing import Optional
from database_manager import DatabaseManager
from match_engine import MatchEngine
from fantasy_engine import FantasyEngine
from ui_console import ConsoleUI
from match_state_manager import MatchStateManager


class CricketSimulator:
    """Main cricket simulator application."""
    
    def __init__(self):
        """Initialize simulator."""
        self.db = DatabaseManager('cricket_data.db')
        self.fantasy_engine = FantasyEngine(self.db)
        self.state_manager = MatchStateManager(self.db)
        self.ui = ConsoleUI()
        self.current_match = None
        self.current_engine = None
    
    def main_menu(self):
        """Display main menu."""
        while True:
            self.ui.print_menu(
                "CRICKET MATCH SIMULATOR",
                [
                    "Create New Match",
                    "Resume Paused Match",
                    "Manage Players",
                    "View Global Rankings",
                    "View Orange Cap Leaders (Batting)",
                    "View Purple Cap Leaders (Bowling)",
                    "View Recent Matches",
                    "Execute Custom SQL",
                    "Exit"
                ]
            )
            
            choice = self.ui.get_choice_input("Select option: ", 
                                            ["1", "2", "3", "4", "5", "6", "7", "8", "9"])
            
            if choice == 1:
                self.create_new_match()
            elif choice == 2:
                self.resume_match()
            elif choice == 3:
                self.manage_players()
            elif choice == 4:
                self.view_global_rankings()
            elif choice == 5:
                self.view_orange_cap_leaders()
            elif choice == 6:
                self.view_purple_cap_leaders()
            elif choice == 7:
                self.view_recent_matches()
            elif choice == 8:
                self.execute_custom_sql()
            elif choice == 9:
                self.ui.print_info("Thank you for using Cricket Match Simulator!")
                break
    
    def view_orange_cap_leaders(self):
        """View Orange Cap Leaders (Fundamental #7)."""
        self.ui.print_header("ORANGE CAP LEADERS (BATTING)")
        
        leaders = self.get_orange_cap_leaders()
        if leaders:
            print(f"{'Rank':<6} {'Player Name':<25} {'Runs':<10} {'Avg':<10}")
            print("-" * 51)
            for idx, leader in enumerate(leaders, 1):
                print(f"{idx:<6} {leader.get('name', 'N/A'):<25} {leader.get('total_runs', 0):<10} " +
                      f"{leader.get('batting_avg', 0):<10.2f}")
        else:
            self.ui.print_info("No batting statistics yet.")
        
        self.ui.pause()
    
    def view_purple_cap_leaders(self):
        """View Purple Cap Leaders (Fundamental #7)."""
        self.ui.print_header("PURPLE CAP LEADERS (BOWLING)")
        
        leaders = self.get_purple_cap_leaders()
        if leaders:
            print(f"{'Rank':<6} {'Player Name':<25} {'Wickets':<10} {'Avg':<10}")
            print("-" * 51)
            for idx, leader in enumerate(leaders, 1):
                print(f"{idx:<6} {leader.get('name', 'N/A'):<25} {leader.get('total_wickets', 0):<10} " +
                      f"{leader.get('bowling_avg', 0):<10.2f}")
        else:
            self.ui.print_info("No bowling statistics yet.")
        
        self.ui.pause()
    
    def manage_players(self):
        """Manage players."""
        while True:
            self.ui.print_menu(
                "MANAGE PLAYERS",
                [
                    "Add New Player",
                    "View All Players",
                    "Delete Player",
                    "Back to Main Menu"
                ]
            )
            
            choice = self.ui.get_choice_input("Select option: ",
                                            ["1", "2", "3", "4"])
            
            if choice == 1:
                self.add_player()
            elif choice == 2:
                self.view_players()
            elif choice == 3:
                self.delete_player()
            elif choice == 4:
                break
    
    def add_player(self):
        """Add a new player."""
        self.ui.print_header("ADD NEW PLAYER")
        
        name = self.ui.get_player_input("Player Name: ")
        batting_avg = self.ui.get_float_input("Batting Average (0-100): ")
        strike_rate = self.ui.get_float_input("Strike Rate (0-200): ")
        runs = self.ui.get_number_input("Career Runs (default 0): ", 0, 100000)
        fours = self.ui.get_number_input("Career 4s (default 0): ", 0, 100000)
        sixes = self.ui.get_number_input("Career 6s (default 0): ", 0, 100000)
        twenties = self.ui.get_number_input("20s (career) (default 0): ", 0, 100000)
        fifties = self.ui.get_number_input("50s (career) (default 0): ", 0, 100000)
        bowling_avg = self.ui.get_float_input("Bowling Average (0-100): ")
        bowling_sr = self.ui.get_float_input("Bowling Strike Rate (balls per wicket): ")
        wickets = self.ui.get_number_input("Career Wickets (default 0): ", 0, 100000)
        economy_rate = self.ui.get_float_input("Economy Rate (0-20): ")

        player_id = self.db.add_player(
            name=name,
            batting_avg=batting_avg,
            strike_rate=strike_rate,
            runs=runs,
            fours=fours,
            sixes=sixes,
            twenties=twenties,
            fifties=fifties,
            bowling_avg=bowling_avg,
            bowling_sr=bowling_sr,
            wickets=wickets,
            economy_rate=economy_rate
        )
        
        if player_id > 0:
            self.ui.print_success(f"Player '{name}' added successfully (ID: {player_id})")
        else:
            self.ui.print_error(f"Failed to add player. Player name may already exist.")
        
        self.ui.pause()
    
    def view_players(self):
        """View all players."""
        self.ui.print_header("ALL PLAYERS")
        
        players = self.db.get_all_players()
        if not players:
            self.ui.print_info("No players in database.")
        else:
            player_list = [
                {
                    'player_id': p.player_id,
                    'name': p.name,
                    'batting_avg': p.batting_avg,
                    'strike_rate': p.strike_rate,
                    'runs': p.runs,
                    'fours': p.fours,
                    'sixes': p.sixes,
                    'twenties': p.twenties,
                    'fifties': p.fifties,
                    'bowling_avg': p.bowling_avg,
                    'bowling_sr': p.bowling_sr,
                    'wickets': p.wickets,
                    'economy_rate': p.economy_rate
                }
                for p in players
            ]
            self.ui.display_player_list(player_list)
        
        self.ui.pause()
    
    def delete_player(self):
        """Delete a player."""
        self.ui.print_header("DELETE PLAYER")
        
        player_id = self.ui.get_number_input("Enter Player ID to delete: ")
        
        if self.db.delete_player(player_id):
            self.ui.print_success("Player deleted successfully.")
        else:
            self.ui.print_error("Failed to delete player.")
        
        self.ui.pause()
    
    def create_new_match(self):
        """Create and run a new match."""
        self.ui.print_header("CREATE NEW MATCH")
        
        match_name = self.ui.get_player_input("Match Name: ")
        total_overs = self.ui.get_number_input("Total Overs: ", 1, 50)
        team_size = self.ui.get_number_input("Team Size (players per side): ", 3, 15)
        
        # Get players
        players = self.db.get_all_players()
        if len(players) < team_size * 2:
            self.ui.print_error(f"Need at least {team_size * 2} players in database.")
            self.ui.pause()
            return
        
        # STEP 2: TOSS - After team selection, conduct the toss
        self.ui.print_header("TOSS")
        self.ui.print_info("Choose which team will CALL the toss:")
        print("1. Team 1")
        print("2. Team 2")
        caller_choice = self.ui.get_number_input("Select caller (1-2): ", 1, 2)

        # Create match placeholder first (we will set toss details when known)
        match_id = self.db.create_match(match_name, total_overs, team_size, 0, 'bat')
        team1_id = self.db.create_team(match_id, "Team 1", 1)
        team2_id = self.db.create_team(match_id, "Team 2", 2)

        # MANUAL DRAFT: Let user select players for each team
        self.draft_teams(team1_id, team2_id, players, team_size)

        # Conduct the toss after both teams are drafted
        caller_name = 'Team 1' if caller_choice == 1 else 'Team 2'
        print(f"{caller_name} will call the toss.")
        print("1. Heads\n2. Tails")
        call_sel = self.ui.get_number_input("Select call (1-2): ", 1, 2)
        call_choice = 'Heads' if call_sel == 1 else 'Tails'

        result = self.ui.animate_coin_toss(caller_name, call_choice)

        caller_team_id = team1_id if caller_choice == 1 else team2_id
        other_team_id = team2_id if caller_choice == 1 else team1_id
        winner_team_id = caller_team_id if result == call_choice else other_team_id
        # Determine loser explicitly to avoid logic mix-up where "other_team_id"
        # was relative to the caller rather than the winner. Use loser_team_id
        # for clear batting/bowling assignment below.
        loser_team_id = team2_id if winner_team_id == team1_id else team1_id

        winner_members = self.db.get_team_members(winner_team_id)
        print("\nSelect player to represent toss winner:")
        for idx, p in enumerate(winner_members, 1):
            print(f"{idx}. {p.name}")
        rep_choice = self.ui.get_number_input(f"Select (1-{len(winner_members)}): ", 1, len(winner_members))
        toss_winner_id = winner_members[rep_choice - 1].player_id

        print("\nToss winner choice: 1=Bat, 2=Bowl")
        decision = self.ui.get_number_input("Choose (1-2): ", 1, 2)
        toss_decision = 'bat' if decision == 1 else 'bowl'

        self.db.update_toss(match_id, toss_winner_id, toss_decision)
        if toss_decision == 'bat':
            self.db.set_team_batting_order(winner_team_id, 1)
            self.db.set_team_batting_order(loser_team_id, 2)
            batting_team_id = winner_team_id
            bowling_team_id = loser_team_id
        else:
            self.db.set_team_batting_order(winner_team_id, 2)
            self.db.set_team_batting_order(loser_team_id, 1)
            batting_team_id = loser_team_id
            bowling_team_id = winner_team_id

        striker_id, non_striker_id, bowler_id = self._prompt_openers_and_bowler(batting_team_id, bowling_team_id)

        self.ui.print_success(f"Match '{match_name}' created (ID: {match_id})")

        # Start match with original teams and toss-selected first innings assignment
        self.run_match(
            match_id,
            team1_id,
            team2_id,
            batting_team_id,
            bowling_team_id,
            total_overs,
            team_size,
            striker_id=striker_id,
            non_striker_id=non_striker_id,
            bowler_id=bowler_id
        )
    
    def draft_teams(self, team1_id: int, team2_id: int, available_players: list, team_size: int):
        """Manual team drafting system - let user select players for each team."""
        team1_players = []
        team2_players = []
        remaining_players = list(available_players)
        jersey_number = 1
        
        self.ui.print_header(f"TEAM DRAFTING - Select {team_size} players for each team")
        print("\n")
        
        # Draft for Team 1
        print(f"Now selecting players for TEAM 1:\n")
        while len(team1_players) < team_size:
            needed = team_size - len(team1_players)
            print(f"Need {needed} more players for Team 1\n")
            
            # Display available players
            print("Available Players:")
            for idx, player in enumerate(remaining_players, 1):
                print(f"{idx}. {player.name} (BAT: {player.batting_avg:.1f}, BOWL: {player.bowling_avg:.1f})")
            print()
            
            # Get selection
            choice = self.ui.get_number_input(f"Select player (1-{len(remaining_players)}): ", 
                                             1, len(remaining_players))
            selected_player = remaining_players[choice - 1]
            
            # Add to team1
            self.db.add_team_member(team1_id, selected_player.player_id, len(team1_players) + 1)
            team1_players.append(selected_player)
            remaining_players.remove(selected_player)
            
            self.ui.print_success(f"✓ {selected_player.name} added to Team 1")
            print("\n")
        
        # Draft for Team 2
        print(f"\nNow selecting players for TEAM 2:\n")
        while len(team2_players) < team_size:
            needed = team_size - len(team2_players)
            print(f"Need {needed} more players for Team 2\n")
            
            # Display available players
            print("Available Players:")
            for idx, player in enumerate(remaining_players, 1):
                print(f"{idx}. {player.name} (BAT: {player.batting_avg:.1f}, BOWL: {player.bowling_avg:.1f})")
            print()
            
            # Get selection
            choice = self.ui.get_number_input(f"Select player (1-{len(remaining_players)}): ", 
                                             1, len(remaining_players))
            selected_player = remaining_players[choice - 1]
            
            # Add to team2
            self.db.add_team_member(team2_id, selected_player.player_id, len(team2_players) + 1)
            team2_players.append(selected_player)
            remaining_players.remove(selected_player)
            
            self.ui.print_success(f"✓ {selected_player.name} added to Team 2")
            print("\n")
        
        # Display final teams
        self.ui.print_header("TEAMS FINALIZED")
        print("TEAM 1:")
        for idx, player in enumerate(team1_players, 1):
            print(f"  {idx}. {player.name}")
        print("\nTEAM 2:")
        for idx, player in enumerate(team2_players, 1):
            print(f"  {idx}. {player.name}")
        print("\n")
        self.ui.pause()
    
    def simulate_ball_manual(self):
        """Manual ball simulation with precise outcome selection."""
        while True:
            self.ui.print_menu(
                "BALL OUTCOME SELECTION",
                [
                    "0 - Dot Ball",
                    "1 - Single",
                    "2 - Double",
                    "3 - Triple",
                    "4 - Boundary",
                    "6 - Six",
                    "Wide",
                    "No Ball",
                    "Wicket - Bowled",
                    "Wicket - Caught",
                    "Wicket - LBW",
                    "Wicket - Run Out",
                    "Dead Ball",
                    "Back to Match"
                ]
            )
            
            choice = self.ui.get_choice_input("Select outcome: ", 
                                             [str(i) for i in range(1, 15)])
            
            if choice == 14:  # Back to Match
                break
            
            # Process the selected outcome
            if choice == 1:  # Dot Ball
                self._apply_ball_outcome(runs_off_bat=0, extras_type='none', wicket_type='none')
            elif choice == 2:  # Single
                self._apply_ball_outcome(runs_off_bat=1, extras_type='none', wicket_type='none')
            elif choice == 3:  # Double
                self._apply_ball_outcome(runs_off_bat=2, extras_type='none', wicket_type='none')
            elif choice == 4:  # Triple
                self._apply_ball_outcome(runs_off_bat=3, extras_type='none', wicket_type='none')
            elif choice == 5:  # Boundary
                self._apply_ball_outcome(runs_off_bat=4, extras_type='none', wicket_type='none')
            elif choice == 6:  # Six
                self._apply_ball_outcome(runs_off_bat=6, extras_type='none', wicket_type='none')
            elif choice == 7:  # Wide
                self._apply_ball_outcome(runs_off_bat=0, extras_type='wide', extra_runs=1, wicket_type='none')
            elif choice == 8:  # No Ball
                self._apply_ball_outcome(runs_off_bat=0, extras_type='no_ball', extra_runs=1, wicket_type='none')
            elif choice == 9:  # Wicket - Bowled
                self._apply_ball_outcome(runs_off_bat=0, extras_type='none', wicket_type='bowled', fielder_id=None)
            elif choice == 10:  # Wicket - Caught
                fielder_id = self._select_fielder()
                self._apply_ball_outcome(runs_off_bat=0, extras_type='none', wicket_type='caught', fielder_id=fielder_id)
            elif choice == 11:  # Wicket - LBW
                self._apply_ball_outcome(runs_off_bat=0, extras_type='none', wicket_type='lbw', fielder_id=None)
            elif choice == 12:  # Wicket - Run Out
                fielder_id = self._select_fielder()
                self._apply_ball_outcome(runs_off_bat=0, extras_type='none', wicket_type='run_out', fielder_id=fielder_id)
            elif choice == 13:  # Dead Ball
                self.ui.print_info("Dead ball: No action taken. Ball will be replayed.")
                continue
            
            # Break after applying outcome
            break
    
    def _select_fielder(self):
        """Select a fielder for caught/run-out dismissals."""
        bowling_team_members = self.db.get_team_members(self.current_engine.bowling_team_id)
        fielders = [p for p in bowling_team_members if p.player_id != self.current_engine.bowler_id]
        
        if not fielders:
            self.ui.print_error("No fielders available (only bowler in team)")
            return None
        
        print("\nSelect Fielder:")
        for idx, fielder in enumerate(fielders, 1):
            print(f"{idx}. {fielder.name}")
        print()
        
        choice = self.ui.get_number_input(f"Select fielder (1-{len(fielders)}): ", 1, len(fielders))
        return fielders[choice - 1].player_id

    def _select_next_batsman(self) -> Optional[int]:
        """Prompt user to select the next batsman from the batting queue."""
        if not self.current_engine:
            return None

        queue_ids = list(self.current_engine.batsmen_queue)
        if not queue_ids:
            self.ui.print_error("No available batsmen in the queue.")
            return None

        print("\nSelect next batsman to come in:")
        options = []
        for idx, pid in enumerate(queue_ids, 1):
            p = self.db.get_player(pid)
            options.append((pid, p.name))
            print(f"{idx}. {p.name}")

        choice = self.ui.get_number_input(f"Select (1-{len(options)}): ", 1, len(options))
        return options[choice - 1][0]

    def _select_next_bowler(self) -> Optional[int]:
        """Prompt user to select the next bowler from the bowling team."""
        if not self.current_engine:
            return None

        bowling_team_members = self.db.get_team_members(self.current_engine.bowling_team_id)
        options = [p for p in bowling_team_members]
        if not options:
            self.ui.print_error("No bowlers available in bowling team.")
            return None

        print("\nSelect next bowler:")
        for idx, p in enumerate(options, 1):
            current_marker = ' (current)' if p.player_id == self.current_engine.bowler_id else ''
            print(f"{idx}. {p.name}{current_marker}")

        choice = self.ui.get_number_input(f"Select (1-{len(options)}): ", 1, len(options))
        return options[choice - 1].player_id
    
    def _apply_ball_outcome(self, runs_off_bat: int = 0, extras_type: str = 'none', 
                           extra_runs: int = 0, wicket_type: str = 'none', fielder_id=None):
        """Apply the selected ball outcome to the match engine."""
        import random
        
        # Increment ball counter
        self.current_engine.current_ball += 1
        
        # Calculate is_dot_ball
        is_dot_ball = (runs_off_bat + extra_runs == 0) and (wicket_type == 'none')
        
        # Save ball to database
        ball_id = self.db.save_ball(
            self.current_engine.current_innings_id,
            self.current_engine.current_over + 1,
            self.current_engine.current_ball,
            self.current_engine.striker_id,
            self.current_engine.bowler_id,
            self.current_engine.non_striker_id,
            runs_off_bat=runs_off_bat,
            extras_type=extras_type,
            extra_runs=extra_runs,
            wicket_type=wicket_type,
            fielder_id=fielder_id,
            is_dot_ball=is_dot_ball
        )
        
        # Create Ball object
        from models import Ball
        ball = Ball(
            ball_id=ball_id,
            innings_id=self.current_engine.current_innings_id,
            over_number=self.current_engine.current_over + 1,
            ball_number=self.current_engine.current_ball,
            striker_id=self.current_engine.striker_id,
            bowler_id=self.current_engine.bowler_id,
            non_striker_id=self.current_engine.non_striker_id,
            runs_off_bat=runs_off_bat,
            extras_type=extras_type,
            extra_runs=extra_runs,
            wicket_type=wicket_type,
            fielder_id=fielder_id,
            is_dot_ball=is_dot_ball
        )
        
        # Update stats
        self.current_engine._update_stats_after_ball(ball)
        
        # Update match state
        self.current_engine.total_runs += (runs_off_bat + extra_runs)
        if wicket_type != 'none':
            self.current_engine.total_wickets += 1
            # Prompt user to select next batsman (if required) and hand over to engine
            next_batter_id = self._select_next_batsman()
            # Delegate wicket handling to engine (it will initialize stats)
            self.current_engine._handle_wicket(wicket_type, fielder_id, chosen_batter_id=next_batter_id)
        
        self.current_engine.ball_history.append(ball)
        
        # Display outcome
        outcome_text = self._format_ball_outcome(ball)
        self.ui.print_success(outcome_text)
        
        # Check match end conditions
        if self.current_engine.total_wickets >= (self.current_engine.team_size - 1):
            self.ui.print_info("ALL OUT!")
            self.current_engine.end_innings()
        elif self.current_engine.innings_number == 2 and self.current_engine._has_chased_target():
            self.ui.print_info("TARGET ACHIEVED! Second innings chase complete.")
            self.current_engine.end_innings()
        elif self.current_engine.current_ball == 6:
            self.ui.print_info(f"End of Over {self.current_engine.current_over + 1}")
            # End over state in engine (strike rotation)
            self.current_engine.end_over()
            # If overs are complete after this over, end the innings.
            if self.current_engine.current_over >= self.current_engine.total_overs:
                self.ui.print_info("Overs complete!")
                self.current_engine.end_innings()
            else:
                chosen_bowler = self._select_next_bowler()
                if chosen_bowler:
                    self.current_engine.bowler_id = chosen_bowler
        elif self.current_engine.current_over >= self.current_engine.total_overs:
            self.ui.print_info("Overs complete!")
            self.current_engine.end_innings()
        else:
            # Rotate strike based on runs (only if not wicket)
            if wicket_type == 'none':
                if (runs_off_bat + extra_runs) % 2 != 0:
                    self.current_engine.striker_id, self.current_engine.non_striker_id = \
                        self.current_engine.non_striker_id, self.current_engine.striker_id
        
        self.ui.pause()
    
    def _format_ball_outcome(self, ball) -> str:
        """Format ball outcome for display."""
        from models import Ball
        
        if ball.wicket_type != 'none':
            striker = self.db.get_player(ball.striker_id)
            return f"WICKET! {striker.name} dismissed ({ball.wicket_type.upper()})"
        elif ball.extras_type == 'wide':
            return f"WIDE - {ball.extra_runs} run(s)"
        elif ball.extras_type == 'no_ball':
            return f"NO BALL - {ball.extra_runs} run(s)"
        elif ball.is_dot_ball:
            return "DOT BALL"
        else:
            total = ball.runs_off_bat + ball.extra_runs
            return f"RUNS SCORED: {total}"

    def _prompt_openers_and_bowler(self, batting_team_id: int, bowling_team_id: int):
        """Prompt user to select two openers from batting team and opening bowler from bowling team.

        Returns tuple (striker_id, non_striker_id, bowler_id).
        """
        batting_members = self.db.get_team_members(batting_team_id)
        bowling_members = self.db.get_team_members(bowling_team_id)

        # Select openers
        self.ui.print_header("SELECT OPENERS FOR NEXT INNINGS")
        print("Select two openers for batting team:")
        for idx, p in enumerate(batting_members, 1):
            print(f"{idx}. {p.name}")

        while True:
            s_choice = self.ui.get_number_input(f"Select Striker (1-{len(batting_members)}): ", 1, len(batting_members))
            ns_choice = self.ui.get_number_input(f"Select Non-Striker (1-{len(batting_members)}): ", 1, len(batting_members))
            if s_choice == ns_choice:
                self.ui.print_error("Striker and Non-Striker cannot be the same player. Please choose again.")
                continue
            striker_id = batting_members[s_choice - 1].player_id
            non_striker_id = batting_members[ns_choice - 1].player_id
            break

        # Select opening bowler
        print("\nSelect opening bowler from bowling team:")
        for idx, p in enumerate(bowling_members, 1):
            print(f"{idx}. {p.name}")
        b_choice = self.ui.get_number_input(f"Select Bowler (1-{len(bowling_members)}): ", 1, len(bowling_members))
        bowler_id = bowling_members[b_choice - 1].player_id

        self.ui.print_success("Openers and bowler selected.")
        return striker_id, non_striker_id, bowler_id

    def run_match(self, match_id: int, team1_id: int, team2_id: int,
                  batting_team_id: int, bowling_team_id: int,
                  total_overs: int, team_size: int,
                  striker_id: Optional[int] = None, non_striker_id: Optional[int] = None,
                  bowler_id: Optional[int] = None):
        """Run a match with original teams and toss-selected innings assignment."""
        if batting_team_id == bowling_team_id:
            self.ui.print_error("Invalid match setup: batting and bowling teams cannot be the same.")
            return

        self.current_engine = MatchEngine(match_id, team1_id, team2_id, total_overs, team_size, self.db)

        # Start first innings with toss-selected batting/bowling teams
        self.current_engine.start_innings(batting_team_id, bowling_team_id, striker_id=striker_id,
                                          non_striker_id=non_striker_id, bowler_id=bowler_id)
        
        # Simulate match
        match_active = True
        while match_active:
            self.display_live_match_scorecard()
            # If innings completed, transition automatically
            if hasattr(self.current_engine, 'innings_complete') and self.current_engine.innings_complete:
                if self.current_engine.innings_number == 2:
                    self.ui.print_info("First innings complete. Starting second innings...")
                    self.current_engine.innings_complete = False
                    batting_tid = self.current_engine.bowling_team_id
                    bowling_tid = self.current_engine.batting_team_id
                    s_id, ns_id, b_id = self._prompt_openers_and_bowler(batting_tid, bowling_tid)
                    self.current_engine.start_innings(batting_tid, bowling_tid, striker_id=s_id, non_striker_id=ns_id, bowler_id=b_id)
                    continue
                else:
                    self.ui.print_info("Match complete. Generating summary...")
                    self.generate_match_summary()
                    match_active = False
                    break

            self.ui.print_menu(
                "MATCH OPTIONS",
                [
                    "Simulate Next Ball (Manual)",
                    "Tables",
                    "Rewind Last Ball",
                    "Substitute Player (Injury)",
                    "Add New Player Mid-Match",
                    "Match Summary",
                    "Pause Match",
                    "End Match"
                ],
                clear_screen=False
            )
            
            choice = self.ui.get_choice_input("Select: ", ["1", "2", "3", "4", "5", "6", "7", "8"])
            
            if choice == 1:
                self.simulate_ball_manual()
            elif choice == 2:
                self.show_tables_menu()
            elif choice == 3:
                self.rewind_last_ball()
            elif choice == 4:
                self.substitute_player_mid_match()
            elif choice == 5:
                self.add_player_mid_match()
            elif choice == 6:
                self.generate_match_summary()
            elif choice == 7:
                if self.current_engine.pause_match():
                    self.state_manager.save_match_state(self.current_engine)
                    self.ui.print_success("Match paused and saved.")
                    match_active = False
                else:
                    self.ui.print_error("Failed to pause match.")
            elif choice == 8:
                match_active = False
                self.ui.print_info("Match ended.")

    def show_tables_menu(self):
        """Show dynamic runtime tables."""
        if not self.current_engine:
            self.ui.print_error("No active match to show tables for.")
            self.ui.pause()
            return

        while True:
            self.ui.print_menu(
                "TABLES",
                [
                    "On-the-go Fours",
                    "Super Strikers",
                    "Fantasy Player score card",
                    "Super Sixes",
                    "Economy Rates",
                    "Back to Match"
                ]
            )
            choice = self.ui.get_choice_input("Select: ", ["1", "2", "3", "4", "5", "6"])

            if choice == 1:
                # On-the-go Fours
                batters = list(self.current_engine.batting_stats.values())
                batters.sort(key=lambda x: x.boundaries, reverse=True)
                rows = []
                for b in batters:
                    if b.boundaries >= 1:
                        player = self.db.get_player(b.player_id)
                        rows.append([player.name, str(b.boundaries), str(b.runs_scored), str(b.balls_faced)])
                self.ui.display_custom_table("On-the-go Fours", ["Player", "Fours", "Runs", "Balls"], rows)
                self.ui.pause()

            elif choice == 2:
                # Super Strikers
                batters = list(self.current_engine.batting_stats.values())
                batters_valid = [b for b in batters if b.balls_faced >= 1]
                batters_valid.sort(key=lambda x: x.strike_rate(), reverse=True)
                rows = []
                for b in batters_valid:
                    player = self.db.get_player(b.player_id)
                    rows.append([player.name, f"{b.strike_rate():.2f}", str(b.runs_scored), str(b.balls_faced)])
                self.ui.display_custom_table("Super Strikers", ["Player", "Strike Rate", "Runs", "Balls"], rows)
                self.ui.pause()

            elif choice == 3:
                # Fantasy Player score card
                summary = self.fantasy_engine.get_live_fantasy_summary(
                    self.current_engine.match_id,
                    self.current_engine.batting_stats,
                    self.current_engine.bowling_stats
                )
                rows = [[str(rank), name, f"{points:.1f}"] for rank, (name, points) in enumerate(summary, 1)]
                self.ui.display_custom_table("Fantasy Player score card", ["Rank", "Player", "Points"], rows)
                self.ui.pause()

            elif choice == 4:
                # Super Sixes
                batters = list(self.current_engine.batting_stats.values())
                batters.sort(key=lambda x: x.sixes, reverse=True)
                rows = []
                for b in batters:
                    if b.sixes >= 1:
                        player = self.db.get_player(b.player_id)
                        rows.append([player.name, str(b.sixes), str(b.runs_scored), str(b.balls_faced)])
                self.ui.display_custom_table("Super Sixes", ["Player", "Sixes", "Runs", "Balls"], rows)
                self.ui.pause()

            elif choice == 5:
                # Economy Rates
                bowlers = list(self.current_engine.bowling_stats.values())
                bowlers_valid = [b for b in bowlers if b.overs_bowled > 0]
                bowlers_valid.sort(key=lambda x: x.economy_rate())
                rows = []
                for b in bowlers_valid:
                    player = self.db.get_player(b.player_id)
                    over_str = f"{int(b.overs_bowled)}.{int((b.overs_bowled % 1) * 10)}" if b.overs_bowled % 1 != 0 else f"{int(b.overs_bowled)}.0"
                    rows.append([player.name, f"{b.economy_rate():.2f}", over_str, str(b.runs_conceded), str(b.wickets_taken)])
                self.ui.display_custom_table("Economy Rates", ["Player", "Economy", "Overs", "Runs", "Wickets"], rows)
                self.ui.pause()

            elif choice == 6:
                break

    def display_live_match_scorecard(self):
        """Display comprehensive live match scorecard (Fundamental #16)."""
        scorecard = self.current_engine.get_current_scorecard()
        self.ui.print_header(f"LIVE MATCH - Over {scorecard['current_over']}.{scorecard['current_ball']}")
        
        print(f"\n{'Date:':<20} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'Score:':<20} {scorecard['total_runs']}/{scorecard['total_wickets']}")
        print(f"{'Overs:':<20} {scorecard['current_over']}.{scorecard['current_ball']} / {scorecard['total_overs']}")
        
        if scorecard['is_chasing']:
            print(f"{'Target:':<20} {scorecard['target_runs']}")
            print(f"{'Required:':<20} {scorecard['required_runs']} in {scorecard['balls_remaining']} balls")
        
        print(f"\n{'Batting:':<20} {scorecard['batting_team_name']}")
        print(f"{'Bowling:':<20} {scorecard['bowling_team_name']}")
        
        # Batter details
        print(f"\n{'Striker:':<20} {scorecard['striker_name']} ({scorecard['striker_runs']} runs, {scorecard['striker_balls']} balls)")
        print(f"{'Non-Striker:':<20} {scorecard['non_striker_name']} ({scorecard['non_striker_runs']} runs, {scorecard['non_striker_balls']} balls)")
        
        # Bowler details
        print(f"{'Bowler:':<20} {scorecard['bowler_name']} ({scorecard['bowler_wickets']}/{scorecard['bowler_runs']} in {scorecard['bowler_overs']})")
        
        # Print batting stats for all batters in current innings
        print(f"\n{'BATTERS':<40} {'R(B)':<10} {'4s':<5} {'6s':<5} {'Status':<10}")
        print('-' * 80)
        for player_id, stats in self.current_engine.batting_stats.items():
            player = self.db.get_player(player_id)
            status = stats.status
            print(f"{player.name:<40} {stats.runs_scored}({stats.balls_faced}){'':<3} {stats.boundaries:<5} {stats.sixes:<5} {status:<10}")
        
        # Print bowling stats for all bowlers in current innings
        print(f"\n{'BOWLERS':<40} {'O':<5} {'R':<5} {'W':<5} {'Dots':<5} {'Eco':<6}")
        print('-' * 80)
        for player_id, stats in self.current_engine.bowling_stats.items():
            player = self.db.get_player(player_id)
            overs_text = f"{int(stats.overs_bowled)}.{int((stats.overs_bowled % 1) * 10)}"
            eco = stats.economy_rate()
            print(f"{player.name:<40} {overs_text:<5} {stats.runs_conceded:<5} {stats.wickets_taken:<5} {stats.dot_balls:<5} {eco:<6.2f}")
        
        # Toss details (if available)
        if hasattr(self.current_engine, 'toss_winner_id'):
            toss_winner = self.db.get_player(self.current_engine.toss_winner_id)
            print(f"\n{'Toss Winner:':<20} {toss_winner.name}")
        
        # Ball history (last 10 balls)
        if self.current_engine.ball_history:
            print(f"\n{'Ball History (Last 10):':<20}")
            for ball in self.current_engine.ball_history[-10:]:
                ball_result = self._format_ball_outcome(ball)
                print(f"  {ball.over_number}.{ball.ball_number}: {ball_result}")
        
        print()
    
    def resume_match(self):
        """Resume a paused match."""
        self.ui.print_header("RESUME PAUSED MATCH")
        
        paused_matches = self.state_manager.get_paused_matches()
        if not paused_matches:
            self.ui.print_info("No paused matches found.")
            self.ui.pause()
            return
        
        for i, match in enumerate(paused_matches, 1):
            print(f"{i}. {match['match_name']} (ID: {match['match_id']})")
        
        choice = self.ui.get_number_input("Select match to resume: ", 1, len(paused_matches))
        
        match_id = paused_matches[choice - 1]['match_id']
        match_state = self.state_manager.load_match_state(match_id)
        
        if match_state:
            self.current_engine = self.state_manager.restore_match_engine(match_state)
            if self.current_engine:
                self.ui.print_success("Match resumed.")
                self.ui.pause()
                # Continue match simulation
                self.run_match_continuation()
            else:
                self.ui.print_error("Failed to restore match.")
        else:
            self.ui.print_error("Failed to load match state.")
        
        self.ui.pause()
    
    def run_match_continuation(self):
        """Continue a resumed match with enhanced options."""
        if not self.current_engine:
            return
        
        match_active = True
        while match_active:
            self.display_live_match_scorecard()
            
            self.ui.print_menu(
                "MATCH OPTIONS",
                [
                    "Simulate Next Ball (Manual)",
                    "Tables",
                    "Rewind Last Ball",
                    "Substitute Player (Injury)",
                    "Match Summary",
                    "Pause Match",
                    "End Match"
                ],
                clear_screen=False
            )
            
            choice = self.ui.get_choice_input("Select: ", ["1", "2", "3", "4", "5", "6", "7"])
            
            if choice == 1:
                self.simulate_ball_manual()
            elif choice == 2:
                self.show_tables_menu()
            elif choice == 3:
                self.rewind_last_ball()
            elif choice == 4:
                self.substitute_player_mid_match()
            elif choice == 5:
                self.generate_match_summary()
            elif choice == 6:
                if self.current_engine.pause_match():
                    self.state_manager.save_match_state(self.current_engine)
                    self.ui.print_success("Match paused and saved.")
                    match_active = False
                else:
                    self.ui.print_error("Failed to pause match.")
            elif choice == 7:
                match_active = False
                self.ui.print_info("Match ended.")
    
    def rewind_last_ball(self):
        """Rewind the last ball played (Fundamental #9).
        
        Handles:
        1. Batsman getting runs even when rewind
        2. Bowler getting runs even when rewind
        3. Bowler getting wicket even when rewind
        4. Batsman name change upon rewind after wicket taken
        5. Total score and wicket count update
        6. Overs count affected correctly
        """
        if not self.current_engine or not self.current_engine.ball_history:
            self.ui.print_error("No balls to rewind.")
            return
        
        try:
            # Get last ball
            last_ball = self.current_engine.ball_history[-1]
            
            self.ui.print_header("REWINDING LAST BALL")
            print(f"Ball to rewind: Over {last_ball.over_number}.{last_ball.ball_number}")
            print(f"Striker: {self.db.get_player(last_ball.striker_id).name}")
            print(f"Bowler: {self.db.get_player(last_ball.bowler_id).name}")
            
            success = self.current_engine.undo_last_ball()
            
            if success:
                self.ui.print_success("Ball successfully rewound!")
                print(f"New Score: {self.current_engine.total_runs}/{self.current_engine.total_wickets}")
                print(f"Overs: {self.current_engine.current_over}.{self.current_engine.current_ball}")
            else:
                self.ui.print_error("Failed to rewind ball programmatically.")
            
        except Exception as e:
            self.ui.print_error(f"Rewind failed: {str(e)}")
        
        self.ui.pause()
    
    def substitute_player_mid_match(self):
        """Substitute a player mid-match for injury (Fundamental #15).
        
        Allows switching either bowler or batter for either side.
        """
        self.ui.print_header("PLAYER SUBSTITUTION (INJURY)")
        
        if not self.current_engine:
            self.ui.print_error("No active match.")
            self.ui.pause()
            return
        
        # Select player type
        self.ui.print_menu("", ["Substitute Batsman", "Substitute Bowler"], clear_screen=False)
        player_type = self.ui.get_choice_input("Choose: ", ["1", "2"])
        
        if player_type == 1:
            # Substitute batsman
            if self.current_engine.striker_id == self.current_engine.current_batsman_id:
                player_to_replace_id = self.current_engine.striker_id
            else:
                player_to_replace_id = self.current_engine.non_striker_id
            
            print(f"Replacing: {self.db.get_player(player_to_replace_id).name}")
            
            # Get available players
            batting_team_id = self.current_engine.batting_team_id
            team_members = self.db.get_team_members(batting_team_id)
            available = [p for p in team_members if p.player_id not in 
                        [self.current_engine.striker_id, self.current_engine.non_striker_id]]
            
            if not available:
                self.ui.print_error("No substitute batsmen available.")
                self.ui.pause()
                return
            
            print("\nAvailable Substitutes:")
            for idx, player in enumerate(available, 1):
                print(f"{idx}. {player.name}")
            
            choice = self.ui.get_number_input(f"Select (1-{len(available)}): ", 1, len(available))
            new_player_id = available[choice - 1].player_id
            
            # Replace in current match state
            if player_to_replace_id == self.current_engine.striker_id:
                self.current_engine.striker_id = new_player_id
            else:
                self.current_engine.non_striker_id = new_player_id
            
            self.ui.print_success(f"Substituted with {self.db.get_player(new_player_id).name}")
        
        elif player_type == 2:
            # Substitute bowler
            print(f"Replacing: {self.db.get_player(self.current_engine.bowler_id).name}")
            
            bowling_team_id = self.current_engine.bowling_team_id
            team_members = self.db.get_team_members(bowling_team_id)
            available = [p for p in team_members if p.player_id != self.current_engine.bowler_id]
            
            if not available:
                self.ui.print_error("No substitute bowlers available.")
                self.ui.pause()
                return
            
            print("\nAvailable Substitutes:")
            for idx, player in enumerate(available, 1):
                print(f"{idx}. {player.name}")
            
            choice = self.ui.get_number_input(f"Select (1-{len(available)}): ", 1, len(available))
            self.current_engine.bowler_id = available[choice - 1].player_id
            
            self.ui.print_success(f"Substituted bowler with {self.db.get_player(self.current_engine.bowler_id).name}")
        
        self.ui.pause()
    
    def add_player_mid_match(self):
        """Add a new player to the database mid-match (Fundamental #14).
        
        Creates player with zero default stats, can be immediately used in match.
        """
        self.ui.print_header("ADD PLAYER MID-MATCH")
        
        name = self.ui.get_player_input("Player Name: ")
        # Default zero stats for mid-match addition
        player_id = self.db.add_player(
            name=name,
            batting_avg=0.0,
            strike_rate=0.0,
            runs=0,
            fours=0,
            sixes=0,
            twenties=0,
            fifties=0,
            bowling_avg=0.0,
            bowling_sr=0.0,
            wickets=0,
            economy_rate=0.0
        )
        
        if player_id > 0:
            self.ui.print_success(f"Player '{name}' added with zero default stats (ID: {player_id})")
        else:
            self.ui.print_error("Failed to add player.")
        
        self.ui.pause()
    
    def display_dismissal_stats(self, batsman_id: int, batting_data: dict):
        """Display detailed player stats when dismissed (Fundamental #11).
        
        Shows: Runs, Balls, SR, 4s, 6s (not saved to database, session-only)
        """
        self.ui.print_header("BATSMAN DISMISSED")
        
        batsman = self.db.get_player(batsman_id)
        runs = batting_data.get('runs', 0)
        balls = batting_data.get('balls', 0)
        fours = batting_data.get('fours', 0)
        sixes = batting_data.get('sixes', 0)
        
        sr = (runs / balls * 100) if balls > 0 else 0
        
        print(f"Player: {batsman.name}")
        print(f"Runs: {runs}")
        print(f"Balls: {balls}")
        print(f"Strike Rate: {sr:.2f}")
        print(f"Fours: {fours}")
        print(f"Sixes: {sixes}")
        print()
    
    def calculate_fantasy_points(self, ball_data: dict, player_role: str) -> float:
        """Calculate fantasy points for player action (Fundamental #7).
        
        Covers:
        - Batting points (runs, boundaries, milestones, duck penalty)
        - Bowling points (wickets, maidens, economy bonus)
        - Fielding points (catches, stumpings, run-outs)
        """
        points = 0.0
        
        if player_role == 'batsman':
            # Batting points
            runs = ball_data.get('runs', 0)
            points += runs * 1.0  # 1 point per run
            
            if 'fours' in ball_data:
                points += ball_data['fours'] * 0.5
            if 'sixes' in ball_data:
                points += ball_data['sixes'] * 1.0
            
            # Milestones
            if runs >= 100:
                points += 16.0
            elif runs >= 50:
                points += 8.0
            elif runs >= 30:
                points += 4.0
            
            # Duck penalty
            if runs == 0 and ball_data.get('dismissed', False):
                points -= 2.0
        
        elif player_role == 'bowler':
            # Bowling points
            wickets = ball_data.get('wickets', 0)
            points += wickets * 25.0
            
            # Maiden overs
            if ball_data.get('maiden_over', False):
                points += 12.0
            
            # Economy bonus (< 5 runs per over)
            economy = ball_data.get('economy_rate', 0)
            if economy < 5:
                points += 6.0
            
            # Milestone bonuses
            if wickets >= 5:
                points += 16.0
            elif wickets >= 4:
                points += 8.0
            elif wickets >= 3:
                points += 4.0
        
        elif player_role == 'fielder':
            # Fielding points
            catches = ball_data.get('catches', 0)
            stumpings = ball_data.get('stumpings', 0)
            run_outs = ball_data.get('run_outs', 0)
            
            points += catches * 8.0
            if catches >= 3:
                points += 4.0
            
            points += stumpings * 12.0
            points += run_outs * 12.0
        
        return points
    
    def get_head_to_head_stats(self, batsman_id: int, bowler_id: int) -> dict:
        """Get head-to-head statistics between batsman and bowler (Fundamental #4).
        
        Returns: Total Runs, SR, Dismissals, Balls faced, Dot Ball %
        """
        stats = {
            'total_runs': 0,
            'strike_rate': 0.0,
            'dismissals': 0,
            'balls_faced': 0,
            'dot_ball_percentage': 0.0
        }
        
        # Get all balls where these two players faced each other
        balls = self.db.get_balls_between_players(batsman_id, bowler_id)
        
        if not balls:
            return stats
        
        dot_balls = 0
        for ball in balls:
            stats['total_runs'] += (ball.runs_off_bat + ball.extra_runs)
            stats['balls_faced'] += 1
            
            if ball.is_dot_ball:
                dot_balls += 1
            
            if ball.wicket_type != 'none':
                stats['dismissals'] += 1
        
        if stats['balls_faced'] > 0:
            stats['strike_rate'] = (stats['total_runs'] / stats['balls_faced']) * 100
            stats['dot_ball_percentage'] = (dot_balls / stats['balls_faced']) * 100
        
        return stats
    
    def generate_match_summary(self):
        """Generate IPL-style match summary (Fundamental #6).
        
        Produces best batting and bowling performances for both teams.
        """
        self.ui.print_header("MATCH SUMMARY")
        
        if not self.current_engine:
            self.ui.print_error("No active match.")
            self.ui.pause()
            return
        
        match_id = self.current_engine.match_id
        innings_list = self.db.get_match_innings(match_id)
        
        print("=" * 100)
        print("BEST BATTING PERFORMANCES (TEAM 1)")
        print("=" * 100)
        
        for innings in innings_list:
            if innings.batting_team_id == self.current_engine.team1_id:
                self._display_best_batsmen(innings.innings_id)
                break
        
        print("\n" + "=" * 100)
        print("BEST BOWLING PERFORMANCES (TEAM 1)")
        print("=" * 100)
        
        for innings in innings_list:
            if innings.bowling_team_id == self.current_engine.team1_id:
                self._display_best_bowlers(innings.innings_id)
                break
        
        print("\n" + "=" * 100)
        print("BEST BATTING PERFORMANCES (TEAM 2)")
        print("=" * 100)
        
        for innings in innings_list:
            if innings.batting_team_id == self.current_engine.team2_id:
                self._display_best_batsmen(innings.innings_id)
                break
        
        print("\n" + "=" * 100)
        print("BEST BOWLING PERFORMANCES (TEAM 2)")
        print("=" * 100)
        
        for innings in innings_list:
            if innings.bowling_team_id == self.current_engine.team2_id:
                self._display_best_bowlers(innings.innings_id)
                break
        
        print("=" * 100)
        self.ui.pause()
    
    def _display_best_batsmen(self, innings_id: int):
        """Display best batsmen for an innings."""
        batsmen_stats = self.db.get_batsmen_stats(innings_id)
        
        if not batsmen_stats:
            print("No batting data available.")
            return
        
        # Sort by runs
        batsmen_stats.sort(key=lambda x: x.get('runs', 0), reverse=True)
        
        for batsman in batsmen_stats[:5]:
            name = self.db.get_player(batsman['player_id']).name
            print(f"{name}: {batsman.get('runs', 0)} runs off {batsman.get('balls', 0)} balls " +
                  f"(SR: {(batsman.get('runs', 0)/batsman.get('balls', 1)*100):.2f}, " +
                  f"4s: {batsman.get('fours', 0)}, 6s: {batsman.get('sixes', 0)})")
    
    def _display_best_bowlers(self, innings_id: int):
        """Display best bowlers for an innings."""
        bowlers_stats = self.db.get_bowlers_stats(innings_id)
        
        if not bowlers_stats:
            print("No bowling data available.")
            return
        
        # Sort by wickets
        bowlers_stats.sort(key=lambda x: x.get('wickets', 0), reverse=True)
        
        for bowler in bowlers_stats[:5]:
            name = self.db.get_player(bowler['player_id']).name
            print(f"{name}: {bowler.get('wickets', 0)} wickets for {bowler.get('runs', 0)} runs " +
                  f"({bowler.get('overs', 0)} overs, Economy: {bowler.get('economy_rate', 0):.2f})")
    
    def get_orange_cap_leaders(self) -> list:
        """Get orange cap leaders (batting) (Fundamental #7)."""
        return self.db.get_top_batsmen(10)
    
    def get_purple_cap_leaders(self) -> list:
        """Get purple cap leaders (bowling) (Fundamental #7)."""
        return self.db.get_top_bowlers(10)
    
    def apply_run_out_mcc_law_38(self, batsman1_id: int, batsman2_id: int, 
                                 stumps_broken_at: str) -> int:
        """Apply MCC Law 38 for run-out dismissal (Fundamental #8).
        
        Determines which batter is out based on:
        - Whether batters have crossed
        - Who is closer to the stumps being broken
        - Whether both reached same crease
        
        Returns: ID of dismissed batsman, or None if neither
        """
        # This would need detailed match state tracking
        # For now, returning a simplified version
        
        if stumps_broken_at == 'bowler_end':
            # If they haven't crossed, batter closest to bowler end is out
            # If they have crossed, batter running towards bowler end is out
            return batsman1_id  # Simplified logic
        else:
            return batsman2_id

    def view_global_rankings(self):
        """View global rankings."""
        self.ui.print_header("GLOBAL RANKINGS")
        
        rankings = self.fantasy_engine.get_global_leaderboard(20)
        if rankings:
            self.ui.display_global_rankings(rankings)
        else:
            self.ui.print_info("No rankings yet.")
        
        self.ui.pause()
    
    def view_recent_matches(self):
        """View recent matches."""
        self.ui.print_header("RECENT MATCHES")
        self.ui.print_info("Feature coming soon.")
        self.ui.pause()
    
    def execute_custom_sql(self):
        """Execute custom SQL query."""
        self.ui.print_header("CUSTOM SQL EXECUTION")
        self.ui.print_info("Warning: Use with caution!")
        
        query = self.ui.get_player_input("Enter SQL query: ")
        
        success, result = self.db.execute_custom_sql(query)
        
        if success:
            self.ui.print_success("Query executed successfully.")
            if isinstance(result, list):
                print(f"Result: {result}")
        else:
            self.ui.print_error(f"Query failed: {result}")
        
        self.ui.pause()
    
    def run(self):
        """Run the application."""
        try:
            self.main_menu()
        except KeyboardInterrupt:
            self.ui.print_info("\nApplication terminated by user.")
        except Exception as e:
            self.ui.print_error(f"An error occurred: {e}")
        finally:
            self.db.close()


def main():
    """Entry point."""
    simulator = CricketSimulator()
    simulator.run()


if __name__ == '__main__':
    main()
