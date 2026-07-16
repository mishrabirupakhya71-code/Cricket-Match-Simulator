"""
Match State Manager for pause/resume functionality.
"""

from typing import Optional, Dict, Any
from database_manager import DatabaseManager
from match_engine import MatchEngine
import json


class MatchStateManager:
    """Manages match state for pause and resume."""
    
    def __init__(self, db: DatabaseManager):
        """Initialize state manager."""
        self.db = db
    
    def save_match_state(self, match_engine: MatchEngine) -> bool:
        """Save complete match state."""
        try:
            state = {
                'match_id': match_engine.match_id,
                'innings_number': match_engine.innings_number,
                'current_innings_id': match_engine.current_innings_id,
                'batting_team_id': match_engine.batting_team_id,
                'bowling_team_id': match_engine.bowling_team_id,
                'current_over': match_engine.current_over,
                'current_ball': match_engine.current_ball,
                'total_runs': match_engine.total_runs,
                'total_wickets': match_engine.total_wickets,
                'striker_id': match_engine.striker_id,
                'non_striker_id': match_engine.non_striker_id,
                'bowler_id': match_engine.bowler_id,
                'batsmen_queue': match_engine.batsmen_queue
            }
            
            # Save to database
            self.db.save_match_state(match_engine.match_id, state)
            return True
        except Exception as e:
            print(f"Error saving match state: {e}")
            return False
    
    def load_match_state(self, match_id: int) -> Optional[Dict[str, Any]]:
        """Load match state for resume."""
        try:
            match = self.db.get_match(match_id)
            if not match:
                return None
            
            # For now, get basic match state
            # In production, load full state from persistent storage
            state = {
                'match_id': match.match_id,
                'match_name': match.match_name,
                'total_overs': match.total_overs,
                'team_size': match.team_size,
                'match_status': match.match_status
            }
            
            return state
        except Exception as e:
            print(f"Error loading match state: {e}")
            return None
    
    def restore_match_engine(self, match_state: Dict[str, Any]) -> Optional[MatchEngine]:
        """Restore match engine from saved state."""
        try:
            match_id = match_state['match_id']
            match = self.db.get_match(match_id)
            
            if not match:
                return None
            
            # Create new match engine
            engine = MatchEngine(
                match_id=match.match_id,
                team1_id=1,  # Would need to load from database
                team2_id=2,  # Would need to load from database
                total_overs=match.total_overs,
                team_size=match.team_size,
                db=self.db
            )
            
            # Restore state
            engine.innings_number = match_state.get('innings_number', 1)
            engine.current_innings_id = match_state.get('current_innings_id')
            engine.batting_team_id = match_state.get('batting_team_id')
            engine.bowling_team_id = match_state.get('bowling_team_id')
            engine.current_over = match_state.get('current_over', 0)
            engine.current_ball = match_state.get('current_ball', 0)
            engine.total_runs = match_state.get('total_runs', 0)
            engine.total_wickets = match_state.get('total_wickets', 0)
            engine.striker_id = match_state.get('striker_id')
            engine.non_striker_id = match_state.get('non_striker_id')
            engine.bowler_id = match_state.get('bowler_id')
            engine.batsmen_queue = match_state.get('batsmen_queue', [])
            
            return engine
        except Exception as e:
            print(f"Error restoring match engine: {e}")
            return None
    
    def get_paused_matches(self) -> list:
        """Get list of paused matches."""
        try:
            self.db.cursor.execute("SELECT * FROM matches WHERE match_status = 'paused'")
            paused = []
            for row in self.db.cursor.fetchall():
                paused.append({
                    'match_id': row[0],
                    'match_name': row[1],
                    'total_overs': row[2],
                    'team_size': row[3]
                })
            return paused
        except Exception:
            return []
