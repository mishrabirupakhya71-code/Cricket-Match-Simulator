"""
Console UI for Cricket Match Simulator.
Real-time scorecards, menus, and interactive display.
"""

from typing import List, Dict, Optional, Tuple
from prettytable import PrettyTable
from colorama import Fore, Back, Style, init
import os
import time

# Initialize colorama for cross-platform colors
init(autoreset=True)


class ConsoleUI:
    """Console user interface for match display."""
    
    def __init__(self):
        """Initialize console UI."""
        self.screen_width = 120
    
    def clear_screen(self):
        """Clear console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        """Print formatted header."""
        self.clear_screen()
        print(f"{Fore.CYAN}{Back.BLACK}{'='*self.screen_width}")
        print(f"{title.center(self.screen_width)}")
        print(f"{'='*self.screen_width}{Style.RESET_ALL}\n")
    
    def print_menu(self, title: str, options: List[str], clear_screen: bool = True):
        """Print menu options."""
        if clear_screen:
            self.print_header(title)
        elif title:
            print(f"{Fore.CYAN}{'='*self.screen_width}")
            print(f"{title.center(self.screen_width)}")
            print(f"{'='*self.screen_width}{Style.RESET_ALL}\n")

        for i, option in enumerate(options, 1):
            print(f"{Fore.GREEN}{i}. {option}{Style.RESET_ALL}")
        print()
    
    def display_scorecard(self, scorecard: Dict):
        """Display current match scorecard."""
        self.clear_screen()
        print(f"{Fore.CYAN}{'='*self.screen_width}")
        print(f"LIVE SCORECARD - {scorecard['match_name']}")
        print(f"{scorecard['batting_team_name']} batting vs {scorecard['bowling_team_name']}")
        print(f"{'='*self.screen_width}{Style.RESET_ALL}\n")
        
        # Main score
        color = Fore.RED if scorecard['all_out'] else Fore.GREEN
        print(f"{color}SCORE: {scorecard['total_runs']}/{scorecard['total_wickets']}{Style.RESET_ALL}")
        print(f"Overs: {scorecard['current_over']}.{scorecard['current_ball']}/{scorecard['total_overs']}\n")
        
        # Striker info
        print(f"{Fore.YELLOW}STRIKER: {scorecard['striker_name']}")
        print(f"Runs: {scorecard['striker_runs']} ({scorecard['striker_balls']} balls){Style.RESET_ALL}\n")
        
        # Non-striker info
        print(f"{Fore.CYAN}NON-STRIKER: {scorecard['non_striker_name']}")
        print(f"Runs: {scorecard['non_striker_runs']} ({scorecard['non_striker_balls']} balls){Style.RESET_ALL}\n")
        
        # Bowler info
        print(f"{Fore.MAGENTA}BOWLER: {scorecard['bowler_name']}")
        print(f"Overs: {scorecard['bowler_overs']} | Runs: {scorecard['bowler_runs']} | Wickets: {scorecard['bowler_wickets']}{Style.RESET_ALL}\n")
        
        # Last 5 balls
        print(f"{Fore.CYAN}Last 5 balls: {scorecard['last_five_balls']}{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}{'='*self.screen_width}{Style.RESET_ALL}")
    
    def display_innings_summary(self, innings_summary: Dict):
        """Display innings summary."""
        self.print_header("INNINGS SUMMARY")
        
        print(f"{Fore.YELLOW}Innings {innings_summary['innings_number']}")
        print(f"Batting Team: {innings_summary['batting_team']}{Style.RESET_ALL}\n")
        
        # Create batting table
        batting_table = PrettyTable()
        batting_table.field_names = ["Batter", "Runs", "Balls", "4s", "6s", "SR", "Status"]
        
        for batter in innings_summary['batting_stats']:
            batting_table.add_row([
                batter['name'],
                batter['runs'],
                batter['balls'],
                batter['fours'],
                batter['sixes'],
                f"{batter['strike_rate']:.1f}",
                batter['status']
            ])
        
        print(batting_table)
        print(f"\nTotal: {innings_summary['total_runs']}/{innings_summary['total_wickets']} "
              f"({innings_summary['overs']} overs)\n")
        
        # Create bowling table
        bowling_table = PrettyTable()
        bowling_table.field_names = ["Bowler", "Overs", "Runs", "Wickets", "Dots", "Economy"]
        
        for bowler in innings_summary['bowling_stats']:
            bowling_table.add_row([
                bowler['name'],
                bowler['overs'],
                bowler['runs'],
                bowler['wickets'],
                bowler['dots'],
                f"{bowler['economy']:.2f}"
            ])
        
        print(bowling_table)
        print()
    
    def display_fantasy_leaderboard(self, leaderboard: List[tuple]):
        """Display fantasy points leaderboard."""
        self.print_header("FANTASY POINTS LEADERBOARD")
        
        table = PrettyTable()
        table.field_names = ["Rank", "Player", "Points"]
        
        for player_name, points, rank in leaderboard:
            table.add_row([rank, player_name, f"{points:.1f}"])
        
        print(table)
        print()
    
    def display_match_awards(self, awards: Dict):
        """Display special match awards."""
        self.print_header("MATCH AWARDS")
        
        if awards['super_striker']:
            player_name, strike_rate = awards['super_striker']
            print(f"{Fore.GREEN}🏆 Super Striker: {player_name} ({strike_rate:.1f}%){Style.RESET_ALL}")
        
        if awards['boundary_rider']:
            player_name, boundaries = awards['boundary_rider']
            print(f"{Fore.YELLOW}🎯 Boundary Rider: {player_name} ({boundaries} fours){Style.RESET_ALL}")
        
        if awards['dot_ball_chieftain']:
            player_name, dots = awards['dot_ball_chieftain']
            print(f"{Fore.CYAN}⚫ Dot Ball Chieftain: {player_name} ({dots} dots){Style.RESET_ALL}")
        
        if awards['mvp']:
            player_name, points = awards['mvp']
            print(f"{Fore.MAGENTA}👑 MVP: {player_name} ({points:.1f} points){Style.RESET_ALL}")
        
        print()
    
    def display_global_rankings(self, rankings: List[Tuple]):
        """Display global rankings."""
        self.print_header("GLOBAL RANKINGS")
        
        table = PrettyTable()
        table.field_names = ["Rank", "Player", "Career Points", "Matches"]
        
        for i, ranking in enumerate(rankings, 1):
            table.add_row([
                i,
                ranking[5],  # Player name
                f"{ranking[2]:.1f}",  # Career points
                ranking[3]   # Matches played
            ])
        
        print(table)
        print()
    
    def display_player_list(self, players: List[Dict]):
        """Display list of players."""
        self.print_header("PLAYERS AVAILABLE")
        
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Runs", "4s", "6s", "Bat Avg", "SR", "Wkts", "Bowl Avg", "Economy"]
        
        for player in players:
            table.add_row([
                player['player_id'],
                player['name'],
                player.get('runs', 0),
                player.get('fours', 0),
                player.get('sixes', 0),
                f"{player.get('batting_avg', 0):.2f}",
                f"{player.get('strike_rate', 0):.2f}",
                player.get('wickets', 0),
                f"{player.get('bowling_avg', 0):.2f}",
                f"{player.get('economy_rate', 0):.2f}"
            ])
        
        print(table)
        print()
    
    def get_player_input(self, prompt: str) -> str:
        """Get player input."""
        return input(f"{Fore.CYAN}{prompt}{Style.RESET_ALL}")
    
    def get_number_input(self, prompt: str, min_val: int = None, max_val: int = None) -> int:
        """Get numeric input with validation."""
        while True:
            try:
                value = int(self.get_player_input(prompt))
                if min_val is not None and value < min_val:
                    print(f"{Fore.RED}Value must be at least {min_val}{Style.RESET_ALL}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"{Fore.RED}Value must be at most {max_val}{Style.RESET_ALL}")
                    continue
                return value
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
    
    def get_float_input(self, prompt: str) -> float:
        """Get float input."""
        while True:
            try:
                return float(self.get_player_input(prompt))
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please enter a valid number.{Style.RESET_ALL}")
    
    def get_choice_input(self, prompt: str, choices: List[str]) -> int:
        """Get choice input."""
        while True:
            choice = self.get_number_input(prompt, 1, len(choices))
            if 1 <= choice <= len(choices):
                return choice
            print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
    
    def print_success(self, message: str):
        """Print success message."""
        print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
    
    def print_error(self, message: str):
        """Print error message."""
        print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")
    
    def print_info(self, message: str):
        """Print info message."""
        print(f"{Fore.CYAN}ℹ {message}{Style.RESET_ALL}")
    
    def pause(self, message: str = "Press Enter to continue..."):
        """Pause and wait for user."""
        input(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

    def animate_coin_toss(self, caller_name: str, call_choice: str = None, rounds: int = 16, write_to_file: bool = True) -> str:
        """Animate a coin toss in ASCII art. Optionally write the frames to a text file.

        - `caller_name`: name of the team or caller displayed during toss.
        - `call_choice`: if provided, the caller selection ('Heads' or 'Tails'). If None, no prompt.
        Returns the result string: 'Heads' or 'Tails'.
        """
        heads = [
            "   _____  ",
            "  /     \\ ",
            " | HEAD  |",
            "  \\_____/ "
        ]
        tails = [
            "   _____  ",
            "  /     \\ ",
            " | TAILS |",
            "  \\_____/ "
        ]

        frames = []
        # Build alternating frames to simulate flip
        for i in range(rounds):
            frames.append(heads if i % 2 == 0 else tails)

        # Final result random
        import random
        result = random.choice(['Heads', 'Tails'])
        final = heads if result == 'Heads' else tails
        frames.append(final)

        out_lines = []
        # Play animation
        for f in frames:
            self.clear_screen()
            print(f"TOSS CALLER: {caller_name}\n")
            for ln in f:
                print(ln)
            out_lines.append('\n'.join(f))
            time.sleep(0.12)

        # Show final result with emphasis
        self.clear_screen()
        print(f"TOSS CALLER: {caller_name}\n")
        for ln in final:
            print(f"{Fore.YELLOW}{ln}{Style.RESET_ALL}")
        print(f"\nResult: {Fore.GREEN}{result}{Style.RESET_ALL}\n")

        if write_to_file:
            try:
                path = os.path.join(os.getcwd(), 'toss_animation.txt')
                with open(path, 'w', encoding='utf-8') as fh:
                    fh.write(f"TOSS by: {caller_name}\n\n")
                    for idx, block in enumerate(out_lines, 1):
                        fh.write(f"Frame {idx}\n")
                        fh.write(block + "\n\n")
                    fh.write(f"Final Result: {result}\n")
            except Exception:
                pass

        return result
