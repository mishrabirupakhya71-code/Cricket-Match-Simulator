"""
Database Manager for SQLite operations.
Handles all CRUD operations, persistence, and custom SQL execution.
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
from models import (
    Player, Match, Team, Innings, Ball, BattingStats, 
    BowlingStats, FantasyStats
)


class DatabaseManager:
    """SQLite database manager."""
    
    def __init__(self, db_path: str = 'cricket_data.db'):
        """Initialize database connection."""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.initialize_database()
    
    def initialize_database(self):
        """Create database connection and initialize schema."""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_schema()
    
    def create_schema(self):
        """Create all database tables."""
        # Players Table - extended batting/bowling schema
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                batting_avg REAL DEFAULT 0.00,
                strike_rate REAL DEFAULT 0.00,
                runs INTEGER DEFAULT 0,
                fours INTEGER DEFAULT 0,
                sixes INTEGER DEFAULT 0,
                twenties INTEGER DEFAULT 0,
                fifties INTEGER DEFAULT 0,
                bowling_avg REAL DEFAULT 0.00,
                bowling_sr REAL DEFAULT 0.00,
                wickets INTEGER DEFAULT 0,
                economy_rate REAL DEFAULT 0.00,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Matches Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                match_id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_name TEXT NOT NULL,
                total_overs INTEGER NOT NULL,
                team_size INTEGER NOT NULL,
                toss_winner_id INTEGER NOT NULL,
                toss_decision TEXT CHECK(toss_decision IN ('bat', 'bowl')),
                match_status TEXT CHECK(match_status IN ('ongoing', 'completed', 'paused')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (toss_winner_id) REFERENCES players(player_id)
            )
        ''')
        
        # Teams Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                team_id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id INTEGER NOT NULL,
                team_name TEXT NOT NULL,
                batting_order INTEGER CHECK(batting_order IN (1, 2)),
                FOREIGN KEY (match_id) REFERENCES matches(match_id),
                UNIQUE(match_id, team_name)
            )
        ''')
        
        # Team Members Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_members (
                team_member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                jersey_number INTEGER,
                FOREIGN KEY (team_id) REFERENCES teams(team_id),
                FOREIGN KEY (player_id) REFERENCES players(player_id),
                UNIQUE(team_id, player_id)
            )
        ''')
        
        # Innings Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS innings (
                innings_id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id INTEGER NOT NULL,
                batting_team_id INTEGER NOT NULL,
                bowling_team_id INTEGER NOT NULL,
                innings_number INTEGER CHECK(innings_number IN (1, 2)),
                total_runs INTEGER DEFAULT 0,
                total_wickets INTEGER DEFAULT 0,
                overs_bowled REAL DEFAULT 0.0,
                status TEXT CHECK(status IN ('ongoing', 'completed')),
                FOREIGN KEY (match_id) REFERENCES matches(match_id),
                FOREIGN KEY (batting_team_id) REFERENCES teams(team_id),
                FOREIGN KEY (bowling_team_id) REFERENCES teams(team_id)
            )
        ''')
        
        # Ball by Ball Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ball_by_ball (
                ball_id INTEGER PRIMARY KEY AUTOINCREMENT,
                innings_id INTEGER NOT NULL,
                over_number INTEGER NOT NULL,
                ball_number INTEGER NOT NULL,
                striker_id INTEGER NOT NULL,
                bowler_id INTEGER NOT NULL,
                non_striker_id INTEGER NOT NULL,
                runs_off_bat INTEGER DEFAULT 0,
                extras_type TEXT CHECK(extras_type IN ('wide', 'no_ball', 'leg_bye', 'bye', 'none')),
                extra_runs INTEGER DEFAULT 0,
                wicket_type TEXT CHECK(wicket_type IN ('bowled', 'caught', 'lbw', 'run_out', 'stumped', 'none')),
                fielder_id INTEGER,
                is_dot_ball INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (innings_id) REFERENCES innings(innings_id),
                FOREIGN KEY (striker_id) REFERENCES players(player_id),
                FOREIGN KEY (bowler_id) REFERENCES players(player_id),
                FOREIGN KEY (non_striker_id) REFERENCES players(player_id),
                FOREIGN KEY (fielder_id) REFERENCES players(player_id)
            )
        ''')
        
        # Batting Stats Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS batting_stats (
                batting_stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                innings_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                runs_scored INTEGER DEFAULT 0,
                balls_faced INTEGER DEFAULT 0,
                boundaries INTEGER DEFAULT 0,
                sixes INTEGER DEFAULT 0,
                status TEXT CHECK(status IN ('not_out', 'bowled', 'caught', 'lbw', 'run_out', 'stumped')),
                FOREIGN KEY (innings_id) REFERENCES innings(innings_id),
                FOREIGN KEY (player_id) REFERENCES players(player_id),
                UNIQUE(innings_id, player_id)
            )
        ''')
        
        # Bowling Stats Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bowling_stats (
                bowling_stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                innings_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                overs_bowled REAL DEFAULT 0.0,
                runs_conceded INTEGER DEFAULT 0,
                wickets_taken INTEGER DEFAULT 0,
                dot_balls INTEGER DEFAULT 0,
                wides INTEGER DEFAULT 0,
                no_balls INTEGER DEFAULT 0,
                FOREIGN KEY (innings_id) REFERENCES innings(innings_id),
                FOREIGN KEY (player_id) REFERENCES players(player_id),
                UNIQUE(innings_id, player_id)
            )
        ''')
        
        # Fantasy Stats Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS fantasy_stats (
                fantasy_stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                match_id INTEGER NOT NULL,
                total_points REAL DEFAULT 0.0,
                run_points REAL DEFAULT 0.0,
                boundary_points REAL DEFAULT 0.0,
                six_points REAL DEFAULT 0.0,
                wicket_points REAL DEFAULT 0.0,
                dismissal_bonus REAL DEFAULT 0.0,
                maiden_over_bonus REAL DEFAULT 0.0,
                strike_rate_penalty REAL DEFAULT 0.0,
                economy_penalty REAL DEFAULT 0.0,
                FOREIGN KEY (player_id) REFERENCES players(player_id),
                FOREIGN KEY (match_id) REFERENCES matches(match_id),
                UNIQUE(player_id, match_id)
            )
        ''')
        
        # Global Rankings Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS global_rankings (
                ranking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER UNIQUE NOT NULL,
                career_points REAL DEFAULT 0.0,
                matches_played INTEGER DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players(player_id)
            )
        ''')
        
        # Sync Log Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sync_log (
                sync_id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id INTEGER,
                sync_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                sync_status TEXT CHECK(sync_status IN ('pending', 'completed', 'failed')),
                device_type TEXT,
                FOREIGN KEY (match_id) REFERENCES matches(match_id)
            )
        ''')
        
        self.conn.commit()
        # Ensure existing database is migrated to new players schema if needed
        self._migrate_players_table()

    def _migrate_players_table(self):
        """Add missing columns to players table if database pre-dates schema changes."""
        try:
            self.cursor.execute("PRAGMA table_info(players)")
            cols = [r[1] for r in self.cursor.fetchall()]
            needed = {
                'batting_avg': 'REAL DEFAULT 0.00',
                'strike_rate': 'REAL DEFAULT 0.00',
                'runs': 'INTEGER DEFAULT 0',
                'fours': 'INTEGER DEFAULT 0',
                'sixes': 'INTEGER DEFAULT 0',
                'twenties': 'INTEGER DEFAULT 0',
                'fifties': 'INTEGER DEFAULT 0',
                'bowling_avg': 'REAL DEFAULT 0.00',
                'bowling_sr': 'REAL DEFAULT 0.00',
                'wickets': 'INTEGER DEFAULT 0',
                'economy_rate': 'REAL DEFAULT 0.00'
            }
            for col, definition in needed.items():
                if col not in cols:
                    sql = f"ALTER TABLE players ADD COLUMN {col} {definition}"
                    try:
                        self.cursor.execute(sql)
                    except Exception:
                        # ignore if cannot add (sqlite limitations)
                        pass
            self.conn.commit()
        except Exception:
            pass
    
    # PLAYER OPERATIONS
    
    def add_player(self, name: str, batting_avg: float = 0.0, strike_rate: float = 0.0,
                   runs: int = 0, fours: int = 0, sixes: int = 0,
                   twenties: int = 0, fifties: int = 0,
                   bowling_avg: float = 0.0, bowling_sr: float = 0.0,
                   wickets: int = 0, economy_rate: float = 0.0) -> int:
        """Add a new player."""
        try:
            self.cursor.execute('''
                INSERT INTO players (
                    name, batting_avg, strike_rate, runs, fours, sixes, twenties, fifties,
                    bowling_avg, bowling_sr, wickets, economy_rate
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, batting_avg, strike_rate, runs, fours, sixes, twenties, fifties,
                  bowling_avg, bowling_sr, wickets, economy_rate))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return -1  # Duplicate player
    
    def get_player(self, player_id: int) -> Optional[Player]:
        """Get player by ID."""
        self.cursor.execute('''
            SELECT player_id, name, batting_avg, strike_rate, runs, fours, sixes,
                   twenties, fifties, bowling_avg, bowling_sr, wickets, economy_rate, created_at
            FROM players WHERE player_id = ?
        ''', (player_id,))
        row = self.cursor.fetchone()
        if row:
            return Player(player_id=row[0], name=row[1], batting_avg=row[2], strike_rate=row[3],
                          runs=row[4], fours=row[5], sixes=row[6], twenties=row[7], fifties=row[8],
                          bowling_avg=row[9], bowling_sr=row[10], wickets=row[11], economy_rate=row[12],
                          created_at=row[13])
        return None
    
    def get_player_by_name(self, name: str) -> Optional[Player]:
        """Get player by name."""
        self.cursor.execute('''
            SELECT player_id, name, batting_avg, strike_rate, runs, fours, sixes,
                   twenties, fifties, bowling_avg, bowling_sr, wickets, economy_rate, created_at
            FROM players WHERE name = ?
        ''', (name,))
        row = self.cursor.fetchone()
        if row:
            return Player(player_id=row[0], name=row[1], batting_avg=row[2], strike_rate=row[3],
                          runs=row[4], fours=row[5], sixes=row[6], twenties=row[7], fifties=row[8],
                          bowling_avg=row[9], bowling_sr=row[10], wickets=row[11], economy_rate=row[12],
                          created_at=row[13])
        return None
    
    def get_all_players(self) -> List[Player]:
        """Get all players."""
        self.cursor.execute('''
            SELECT player_id, name, batting_avg, strike_rate, runs, fours, sixes,
                   twenties, fifties, bowling_avg, bowling_sr, wickets, economy_rate, created_at
            FROM players ORDER BY name
        ''')
        players = []
        for row in self.cursor.fetchall():
            players.append(Player(player_id=row[0], name=row[1], batting_avg=row[2], strike_rate=row[3],
                                  runs=row[4], fours=row[5], sixes=row[6], twenties=row[7], fifties=row[8],
                                  bowling_avg=row[9], bowling_sr=row[10], wickets=row[11], economy_rate=row[12],
                                  created_at=row[13]))
        return players
    
    def delete_player(self, player_id: int) -> bool:
        """Delete a player."""
        try:
            self.cursor.execute('DELETE FROM players WHERE player_id = ?', (player_id,))
            self.conn.commit()
            return True
        except Exception:
            return False

    def reset_player_stats(self, player_id: Optional[int] = None) -> int:
        """Reset player career stats to zero. If player_id is None, reset all players.

        Also resets any per-innings batting_stats and bowling_stats rows for the player(s).
        Returns number of player rows affected.
        """
        try:
            if player_id is None:
                # Reset players table
                self.cursor.execute('''
                    UPDATE players SET
                        batting_avg = 0.00,
                        strike_rate = 0.00,
                        runs = 0,
                        fours = 0,
                        sixes = 0,
                        twenties = 0,
                        fifties = 0,
                        bowling_avg = 0.00,
                        bowling_sr = 0.00,
                        wickets = 0,
                        economy_rate = 0.00
                ''')
                players_updated = self.cursor.rowcount
                # Zero batting and bowling per-innings stats
                self.cursor.execute('UPDATE batting_stats SET runs_scored = 0, balls_faced = 0, boundaries = 0, sixes = 0')
                self.cursor.execute('UPDATE bowling_stats SET overs_bowled = 0.0, runs_conceded = 0, wickets_taken = 0, dot_balls = 0, wides = 0, no_balls = 0')
            else:
                self.cursor.execute('''
                    UPDATE players SET
                        batting_avg = 0.00,
                        strike_rate = 0.00,
                        runs = 0,
                        fours = 0,
                        sixes = 0,
                        twenties = 0,
                        fifties = 0,
                        bowling_avg = 0.00,
                        bowling_sr = 0.00,
                        wickets = 0,
                        economy_rate = 0.00
                    WHERE player_id = ?
                ''', (player_id,))
                players_updated = self.cursor.rowcount
                self.cursor.execute('UPDATE batting_stats SET runs_scored = 0, balls_faced = 0, boundaries = 0, sixes = 0 WHERE player_id = ?', (player_id,))
                self.cursor.execute('UPDATE bowling_stats SET overs_bowled = 0.0, runs_conceded = 0, wickets_taken = 0, dot_balls = 0, wides = 0, no_balls = 0 WHERE player_id = ?', (player_id,))

            self.conn.commit()
            return players_updated if players_updated is not None else 0
        except Exception:
            return 0
    
    # MATCH OPERATIONS
    
    def create_match(self, match_name: str, total_overs: int, team_size: int,
                     toss_winner_id: int, toss_decision: str) -> int:
        """Create a new match."""
        self.cursor.execute('''
            INSERT INTO matches (match_name, total_overs, team_size, toss_winner_id, toss_decision, match_status)
            VALUES (?, ?, ?, ?, ?, 'ongoing')
        ''', (match_name, total_overs, team_size, toss_winner_id, toss_decision))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_match(self, match_id: int) -> Optional[Match]:
        """Get match by ID."""
        self.cursor.execute('SELECT * FROM matches WHERE match_id = ?', (match_id,))
        row = self.cursor.fetchone()
        if row:
            return Match(match_id=row[0], match_name=row[1], total_overs=row[2],
                        team_size=row[3], toss_winner_id=row[4], toss_decision=row[5],
                        match_status=row[6])
        return None
    
    def update_match_status(self, match_id: int, status: str) -> bool:
        """Update match status."""
        try:
            self.cursor.execute('UPDATE matches SET match_status = ? WHERE match_id = ?',
                              (status, match_id))
            self.conn.commit()
            return True
        except Exception:
            return False

    def update_toss(self, match_id: int, toss_winner_id: int, toss_decision: str) -> bool:
        """Update toss winner and decision for a match."""
        try:
            self.cursor.execute('UPDATE matches SET toss_winner_id = ?, toss_decision = ? WHERE match_id = ?',
                                (toss_winner_id, toss_decision, match_id))
            self.conn.commit()
            return True
        except Exception:
            return False

    def set_team_batting_order(self, team_id: int, batting_order: int) -> bool:
        """Set batting order (1 or 2) for a team in a match."""
        try:
            self.cursor.execute('UPDATE teams SET batting_order = ? WHERE team_id = ?', (batting_order, team_id))
            self.conn.commit()
            return True
        except Exception:
            return False
    
    # TEAM OPERATIONS
    
    def create_team(self, match_id: int, team_name: str, batting_order: int) -> int:
        """Create a team."""
        self.cursor.execute('''
            INSERT INTO teams (match_id, team_name, batting_order)
            VALUES (?, ?, ?)
        ''', (match_id, team_name, batting_order))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def add_team_member(self, team_id: int, player_id: int, jersey_number: int) -> bool:
        """Add player to team."""
        try:
            self.cursor.execute('''
                INSERT INTO team_members (team_id, player_id, jersey_number)
                VALUES (?, ?, ?)
            ''', (team_id, player_id, jersey_number))
            self.conn.commit()
            return True
        except Exception:
            return False
    
    def get_team_members(self, team_id: int) -> List[Player]:
        """Get all members of a team."""
        self.cursor.execute('''
            SELECT p.* FROM players p
            JOIN team_members tm ON p.player_id = tm.player_id
            WHERE tm.team_id = ?
        ''', (team_id,))
        players = []
        for row in self.cursor.fetchall():
            # Map to new Player fields assuming same column order as players select
            players.append(Player(player_id=row[0], name=row[1], batting_avg=row[2], strike_rate=row[3],
                                  runs=row[4], fours=row[5], sixes=row[6], twenties=row[7], fifties=row[8],
                                  bowling_avg=row[9], bowling_sr=row[10], wickets=row[11], economy_rate=row[12],
                                  created_at=row[13]))
        return players

    # Ball delete (used by rewind)
    def delete_ball(self, ball_id: int) -> bool:
        """Delete a ball record by ID."""
        try:
            self.cursor.execute('DELETE FROM ball_by_ball WHERE ball_id = ?', (ball_id,))
            self.conn.commit()
            return True
        except Exception:
            return False

    def get_balls_between_players(self, batsman_id: int, bowler_id: int) -> List[Ball]:
        """Return all ball records where batsman faced the bowler."""
        self.cursor.execute('''
            SELECT * FROM ball_by_ball WHERE striker_id = ? AND bowler_id = ?
            ORDER BY over_number, ball_number
        ''', (batsman_id, bowler_id))
        balls = []
        for row in self.cursor.fetchall():
            balls.append(Ball(
                ball_id=row[0], innings_id=row[1], over_number=row[2], ball_number=row[3],
                striker_id=row[4], bowler_id=row[5], non_striker_id=row[6],
                runs_off_bat=row[7], extras_type=row[8], extra_runs=row[9],
                wicket_type=row[10], fielder_id=row[11], is_dot_ball=bool(row[12])
            ))
        return balls

    def get_top_batsmen(self, limit: int = 10) -> List[Dict]:
        """Return top batsmen by total runs across batting_stats."""
        self.cursor.execute('''
            SELECT p.player_id, p.name, SUM(bs.runs_scored) as total_runs, AVG(COALESCE(p.batting_avg,0)) as batting_avg
            FROM batting_stats bs
            JOIN players p ON bs.player_id = p.player_id
            GROUP BY p.player_id
            ORDER BY total_runs DESC
            LIMIT ?
        ''', (limit,))
        rows = self.cursor.fetchall()
        leaders = []
        for r in rows:
            leaders.append({'player_id': r[0], 'name': r[1], 'total_runs': r[2], 'batting_avg': r[3]})
        return leaders

    def get_top_bowlers(self, limit: int = 10) -> List[Dict]:
        """Return top bowlers by total wickets across bowling_stats."""
        self.cursor.execute('''
            SELECT p.player_id, p.name, SUM(bs.wickets_taken) as total_wickets, AVG(COALESCE(p.bowling_avg,0)) as bowling_avg
            FROM bowling_stats bs
            JOIN players p ON bs.player_id = p.player_id
            GROUP BY p.player_id
            ORDER BY total_wickets DESC
            LIMIT ?
        ''', (limit,))
        rows = self.cursor.fetchall()
        leaders = []
        for r in rows:
            leaders.append({'player_id': r[0], 'name': r[1], 'total_wickets': r[2], 'bowling_avg': r[3]})
        return leaders
    
    def get_team(self, team_id: int) -> Optional[Team]:
        """Get team metadata by ID."""
        self.cursor.execute('SELECT * FROM teams WHERE team_id = ?', (team_id,))
        row = self.cursor.fetchone()
        if row:
            return Team(team_id=row[0], match_id=row[1], team_name=row[2], batting_order=row[3])
        return None

    def create_innings(self, match_id: int, batting_team_id: int,
                       bowling_team_id: int, innings_number: int) -> int:
        """Create a new innings record."""
        self.cursor.execute('''
            INSERT INTO innings (
                match_id, batting_team_id, bowling_team_id, innings_number, status
            ) VALUES (?, ?, ?, ?, 'ongoing')
        ''', (match_id, batting_team_id, bowling_team_id, innings_number))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_innings(self, innings_id: int) -> Optional[Innings]:
        """Get innings by ID."""
        self.cursor.execute('SELECT * FROM innings WHERE innings_id = ?', (innings_id,))
        row = self.cursor.fetchone()
        if row:
            return Innings(innings_id=row[0], match_id=row[1], batting_team_id=row[2],
                          bowling_team_id=row[3], innings_number=row[4],
                          total_runs=row[5], total_wickets=row[6], overs_bowled=row[7],
                          status=row[8])
        return None

    def update_innings_score(self, innings_id: int, total_runs: int,
                            total_wickets: int, overs_bowled: float) -> bool:
        """Update innings score."""
        try:
            self.cursor.execute('''
                UPDATE innings SET total_runs = ?, total_wickets = ?, overs_bowled = ?
                WHERE innings_id = ?
            ''', (total_runs, total_wickets, overs_bowled, innings_id))
            self.conn.commit()
            return True
        except Exception:
            return False
    
    def complete_innings(self, innings_id: int) -> bool:
        """Mark innings as completed."""
        try:
            self.cursor.execute('UPDATE innings SET status = ? WHERE innings_id = ?',
                              ('completed', innings_id))
            self.conn.commit()
            return True
        except Exception:
            return False
    
    # BALL OPERATIONS
    
    def save_ball(self, innings_id: int, over_number: int, ball_number: int,
                  striker_id: int, bowler_id: int, non_striker_id: int,
                  runs_off_bat: int = 0, extras_type: str = 'none', extra_runs: int = 0,
                  wicket_type: str = 'none', fielder_id: Optional[int] = None,
                  is_dot_ball: bool = False) -> int:
        """Save ball data."""
        self.cursor.execute('''
            INSERT INTO ball_by_ball
            (innings_id, over_number, ball_number, striker_id, bowler_id, non_striker_id,
             runs_off_bat, extras_type, extra_runs, wicket_type, fielder_id, is_dot_ball)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (innings_id, over_number, ball_number, striker_id, bowler_id, non_striker_id,
              runs_off_bat, extras_type, extra_runs, wicket_type, fielder_id, int(is_dot_ball)))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_balls_in_innings(self, innings_id: int) -> List[Ball]:
        """Get all balls in innings."""
        self.cursor.execute('''
            SELECT * FROM ball_by_ball WHERE innings_id = ? ORDER BY over_number, ball_number
        ''', (innings_id,))
        balls = []
        for row in self.cursor.fetchall():
            balls.append(Ball(
                ball_id=row[0], innings_id=row[1], over_number=row[2], ball_number=row[3],
                striker_id=row[4], bowler_id=row[5], non_striker_id=row[6],
                runs_off_bat=row[7], extras_type=row[8], extra_runs=row[9],
                wicket_type=row[10], fielder_id=row[11], is_dot_ball=bool(row[12])
            ))
        return balls
    
    # BATTING STATS OPERATIONS
    
    def save_batting_stats(self, innings_id: int, player_id: int,
                          runs_scored: int = 0, balls_faced: int = 0,
                          boundaries: int = 0, sixes: int = 0,
                          status: str = 'not_out') -> int:
        """Save or update batting stats."""
        try:
            self.cursor.execute('''
                INSERT INTO batting_stats
                (innings_id, player_id, runs_scored, balls_faced, boundaries, sixes, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(innings_id, player_id) DO UPDATE SET
                runs_scored = excluded.runs_scored,
                balls_faced = excluded.balls_faced,
                boundaries = excluded.boundaries,
                sixes = excluded.sixes,
                status = excluded.status
            ''', (innings_id, player_id, runs_scored, balls_faced, boundaries, sixes, status))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            return -1
    
    def get_batting_stats(self, innings_id: int, player_id: int) -> Optional[BattingStats]:
        """Get batting stats for player in innings."""
        self.cursor.execute('''
            SELECT * FROM batting_stats WHERE innings_id = ? AND player_id = ?
        ''', (innings_id, player_id))
        row = self.cursor.fetchone()
        if row:
            return BattingStats(
                batting_stat_id=row[0], innings_id=row[1], player_id=row[2],
                runs_scored=row[3], balls_faced=row[4], boundaries=row[5],
                sixes=row[6], status=row[7]
            )
        return None
    
    # BOWLING STATS OPERATIONS
    
    def save_bowling_stats(self, innings_id: int, player_id: int,
                          overs_bowled: float = 0.0, runs_conceded: int = 0,
                          wickets_taken: int = 0, dot_balls: int = 0,
                          wides: int = 0, no_balls: int = 0) -> int:
        """Save or update bowling stats."""
        try:
            self.cursor.execute('''
                INSERT INTO bowling_stats
                (innings_id, player_id, overs_bowled, runs_conceded, wickets_taken, dot_balls, wides, no_balls)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(innings_id, player_id) DO UPDATE SET
                overs_bowled = excluded.overs_bowled,
                runs_conceded = excluded.runs_conceded,
                wickets_taken = excluded.wickets_taken,
                dot_balls = excluded.dot_balls,
                wides = excluded.wides,
                no_balls = excluded.no_balls
            ''', (innings_id, player_id, overs_bowled, runs_conceded, wickets_taken,
                  dot_balls, wides, no_balls))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception:
            return -1
    
    def get_bowling_stats(self, innings_id: int, player_id: int) -> Optional[BowlingStats]:
        """Get bowling stats for player in innings."""
        self.cursor.execute('''
            SELECT * FROM bowling_stats WHERE innings_id = ? AND player_id = ?
        ''', (innings_id, player_id))
        row = self.cursor.fetchone()
        if row:
            return BowlingStats(
                bowling_stat_id=row[0], innings_id=row[1], player_id=row[2],
                overs_bowled=row[3], runs_conceded=row[4], wickets_taken=row[5],
                dot_balls=row[6], wides=row[7], no_balls=row[8]
            )
        return None

    def get_match_innings(self, match_id: int) -> List[Innings]:
        """Return innings records for a match."""
        self.cursor.execute('SELECT * FROM innings WHERE match_id = ? ORDER BY innings_number', (match_id,))
        rows = self.cursor.fetchall()
        innings_list = []
        for row in rows:
            innings_list.append(Innings(innings_id=row[0], match_id=row[1], batting_team_id=row[2],
                                        bowling_team_id=row[3], innings_number=row[4], total_runs=row[5],
                                        total_wickets=row[6], overs_bowled=row[7], status=row[8]))
        return innings_list

    def get_batsmen_stats(self, innings_id: int) -> List[Dict]:
        """Return batting stats for all players in an innings as list of dicts."""
        self.cursor.execute('''
            SELECT player_id, runs_scored, balls_faced, boundaries, sixes
            FROM batting_stats WHERE innings_id = ?
        ''', (innings_id,))
        rows = self.cursor.fetchall()
        stats = []
        for r in rows:
            stats.append({'player_id': r[0], 'runs': r[1], 'balls': r[2], 'fours': r[3], 'sixes': r[4]})
        return stats

    def get_bowlers_stats(self, innings_id: int) -> List[Dict]:
        """Return bowling stats for all players in an innings as list of dicts."""
        self.cursor.execute('''
            SELECT player_id, overs_bowled, runs_conceded, wickets_taken, dot_balls
            FROM bowling_stats WHERE innings_id = ?
        ''', (innings_id,))
        rows = self.cursor.fetchall()
        stats = []
        for r in rows:
            overs = r[1]
            runs = r[2]
            wickets = r[3]
            economy = (runs / overs) if overs and overs > 0 else 0.0
            stats.append({'player_id': r[0], 'overs': overs, 'runs': runs, 'wickets': wickets, 'dots': r[4], 'economy_rate': economy})
        return stats
    
    # FANTASY STATS OPERATIONS
    
    def save_fantasy_stats(self, player_id: int, match_id: int,
                          total_points: float = 0.0, run_points: float = 0.0,
                          boundary_points: float = 0.0, six_points: float = 0.0,
                          wicket_points: float = 0.0, dismissal_bonus: float = 0.0,
                          maiden_over_bonus: float = 0.0, strike_rate_penalty: float = 0.0,
                          economy_penalty: float = 0.0) -> int:
        """Save fantasy stats."""
        try:
            self.cursor.execute('''
                INSERT INTO fantasy_stats
                (player_id, match_id, total_points, run_points, boundary_points, six_points,
                 wicket_points, dismissal_bonus, maiden_over_bonus, strike_rate_penalty, economy_penalty)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(player_id, match_id) DO UPDATE SET
                total_points = excluded.total_points,
                run_points = excluded.run_points,
                boundary_points = excluded.boundary_points,
                six_points = excluded.six_points,
                wicket_points = excluded.wicket_points,
                dismissal_bonus = excluded.dismissal_bonus,
                maiden_over_bonus = excluded.maiden_over_bonus,
                strike_rate_penalty = excluded.strike_rate_penalty,
                economy_penalty = excluded.economy_penalty
            ''', (player_id, match_id, total_points, run_points, boundary_points, six_points,
                  wicket_points, dismissal_bonus, maiden_over_bonus, strike_rate_penalty, economy_penalty))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception:
            return -1
    
    def get_fantasy_stats(self, player_id: int, match_id: int) -> Optional[FantasyStats]:
        """Get fantasy stats."""
        self.cursor.execute('''
            SELECT * FROM fantasy_stats WHERE player_id = ? AND match_id = ?
        ''', (player_id, match_id))
        row = self.cursor.fetchone()
        if row:
            return FantasyStats(
                fantasy_stat_id=row[0], player_id=row[1], match_id=row[2],
                total_points=row[3], run_points=row[4], boundary_points=row[5],
                six_points=row[6], wicket_points=row[7], dismissal_bonus=row[8],
                maiden_over_bonus=row[9], strike_rate_penalty=row[10], economy_penalty=row[11]
            )
        return None
    
    # CUSTOM SQL OPERATIONS
    
    def execute_custom_sql(self, query: str) -> Tuple[bool, Any]:
        """Execute custom SQL query."""
        try:
            if query.strip().upper().startswith('SELECT'):
                self.cursor.execute(query)
                return True, self.cursor.fetchall()
            else:
                self.cursor.execute(query)
                self.conn.commit()
                return True, "Query executed successfully"
        except Exception as e:
            return False, str(e)
    
    # MATCH STATE PERSISTENCE
    
    def save_match_state(self, match_id: int, state: Dict) -> bool:
        """Save match state for pause/resume."""
        try:
            # Update match and innings data
            match = self.get_match(match_id)
            if match:
                self.update_match_status(match_id, 'paused')
            return True
        except Exception:
            return False
    
    def get_match_state(self, match_id: int) -> Optional[Dict]:
        """Retrieve match state for resumption."""
        try:
            match = self.get_match(match_id)
            if not match:
                return None
            
            state = {
                'match': match,
                'match_status': match.match_status
            }
            return state
        except Exception:
            return None
    
    # SYNC OPERATIONS
    
    def record_sync(self, match_id: int, status: str, device_type: str) -> int:
        """Record sync operation."""
        self.cursor.execute('''
            INSERT INTO sync_log (match_id, sync_status, device_type)
            VALUES (?, ?, ?)
        ''', (match_id, status, device_type))
        self.conn.commit()
        return self.cursor.lastrowid
    
    # GLOBAL RANKINGS
    
    def update_global_ranking(self, player_id: int, career_points: float) -> bool:
        """Update global ranking."""
        try:
            self.cursor.execute('''
                INSERT INTO global_rankings (player_id, career_points, matches_played)
                VALUES (?, ?, 1)
                ON CONFLICT(player_id) DO UPDATE SET
                career_points = excluded.career_points,
                matches_played = matches_played + 1,
                last_updated = CURRENT_TIMESTAMP
            ''', (player_id, career_points))
            self.conn.commit()
            return True
        except Exception:
            return False
    
    def get_global_leaderboard(self, limit: int = 10) -> List[Tuple]:
        """Get global leaderboard."""
        self.cursor.execute('''
            SELECT gr.*, p.name FROM global_rankings gr
            JOIN players p ON gr.player_id = p.player_id
            ORDER BY gr.career_points DESC
            LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
