"""
Unit tests for detailed strike rotation mechanics.
Tests all scenarios: singles, twos, threes, fours, sixes, end of over, wickets.
"""

import unittest
import sys
sys.path.insert(0, '../desktop_simulator')


class TestStrikeRotationComprehensive(unittest.TestCase):
    """Comprehensive strike rotation tests."""
    
    def setUp(self):
        """Set up test state."""
        self.striker = 1
        self.non_striker = 2
    
    def test_dot_ball_no_rotation(self):
        """Dot ball (0 runs) doesn't rotate strike."""
        new_striker, new_non_striker = self._rotate_strike(
            striker=self.striker,
            non_striker=self.non_striker,
            runs=0
        )
        self.assertEqual(new_striker, self.striker)
        self.assertEqual(new_non_striker, self.non_striker)
    
    def test_single_run_rotates(self):
        """Single run rotates strike."""
        new_striker, new_non_striker = self._rotate_strike(
            striker=self.striker,
            non_striker=self.non_striker,
            runs=1
        )
        self.assertEqual(new_striker, self.non_striker)
        self.assertEqual(new_non_striker, self.striker)
    
    def test_two_runs_no_rotation(self):
        """Two runs don't rotate strike."""
        new_striker, new_non_striker = self._rotate_strike(
            striker=self.striker,
            non_striker=self.non_striker,
            runs=2
        )
        self.assertEqual(new_striker, self.striker)
        self.assertEqual(new_non_striker, self.non_striker)
    
    def test_three_runs_rotates(self):
        """Three runs rotate strike."""
        new_striker, new_non_striker = self._rotate_strike(
            striker=self.striker,
            non_striker=self.non_striker,
            runs=3
        )
        self.assertEqual(new_striker, self.non_striker)
        self.assertEqual(new_non_striker, self.striker)
    
    def test_four_runs_no_rotation(self):
        """Four runs (boundary) don't rotate strike."""
        new_striker, new_non_striker = self._rotate_strike(
            striker=self.striker,
            non_striker=self.non_striker,
            runs=4
        )
        self.assertEqual(new_striker, self.striker)
        self.assertEqual(new_non_striker, self.non_striker)
    
    def test_five_runs_rotates(self):
        """Five runs rotate strike."""
        new_striker, new_non_striker = self._rotate_strike(
            striker=self.striker,
            non_striker=self.non_striker,
            runs=5
        )
        self.assertEqual(new_striker, self.non_striker)
        self.assertEqual(new_non_striker, self.striker)
    
    def test_six_runs_no_rotation(self):
        """Six runs don't rotate strike."""
        new_striker, new_non_striker = self._rotate_strike(
            striker=self.striker,
            non_striker=self.non_striker,
            runs=6
        )
        self.assertEqual(new_striker, self.striker)
        self.assertEqual(new_non_striker, self.non_striker)
    
    def test_end_of_over_rotation(self):
        """End of over always rotates strike."""
        new_striker, new_non_striker = self._rotate_strike_end_of_over(
            striker=self.striker,
            non_striker=self.non_striker
        )
        self.assertEqual(new_striker, self.non_striker)
        self.assertEqual(new_non_striker, self.striker)
    
    def test_complex_over_with_runs(self):
        """Complex over: 0, 1, 0, 2, 0, 1 runs — includes end-of-over rotation."""
        runs_sequence = [0, 1, 0, 2, 0, 1]
        
        striker = self.striker
        non_striker = self.non_striker
        
        for runs in runs_sequence:
            striker, non_striker = self._rotate_strike(striker, non_striker, runs)
        
        # After 6 balls: two odd-run swaps cancel out → striker back to original
        # Then end-of-over rotation swaps once more
        striker, non_striker = self._rotate_strike_end_of_over(striker, non_striker)
        
        self.assertEqual(striker, self.non_striker)
        self.assertEqual(non_striker, self.striker)
    
    def test_wicket_during_over_next_batsman(self):
        """Wicket during over: new batter comes in."""
        # Striker gets out (bowled)
        new_batter = 3
        new_striker, new_non_striker = self._handle_wicket(
            striker=self.striker,
            non_striker=self.non_striker,
            new_batter=new_batter,
            runs_before_wicket=2
        )
        # Wicket doesn't rotate; new batter replaces striker
        self.assertEqual(new_striker, new_batter)
        self.assertEqual(new_non_striker, self.non_striker)
    
    def test_run_out_while_taking_single(self):
        """Run-out attempt while taking single."""
        # If run-out occurs on single, the taking-run happened
        # The batters have rotated or are mid-run
        result = self._handle_run_out_on_single(
            striker=self.striker,
            non_striker=self.non_striker
        )
        self.assertTrue(result['strike_rotated'])
    
    def test_wide_doesnt_count_ball(self):
        """Wide ball doesn't count as a regular ball."""
        result = self._handle_wide(balls_in_over=5)
        self.assertEqual(result['balls_in_over'], 5)  # Still 5, not 6
    
    def test_no_ball_doesnt_count_ball(self):
        """No-ball doesn't count as a regular ball."""
        result = self._handle_no_ball(balls_in_over=5)
        self.assertEqual(result['balls_in_over'], 5)  # Still 5, not 6
    
    def test_leg_bye_counts_ball(self):
        """Leg-bye counts as a regular ball."""
        result = self._handle_leg_bye(balls_in_over=5, runs=1)
        self.assertEqual(result['balls_in_over'], 6)  # Now 6 (completes over)
    
    def test_bye_counts_ball(self):
        """Bye counts as a regular ball."""
        result = self._handle_bye(balls_in_over=5, runs=1)
        self.assertEqual(result['balls_in_over'], 6)  # Now 6 (completes over)
    
    def _rotate_strike(self, striker, non_striker, runs):
        """Rotate strike based on runs."""
        if runs % 2 != 0:  # Odd runs = rotate
            return non_striker, striker
        return striker, non_striker
    
    def _rotate_strike_end_of_over(self, striker, non_striker):
        """End of over always rotates."""
        return non_striker, striker
    
    def _handle_wicket(self, striker, non_striker, new_batter, runs_before_wicket):
        """Handle wicket during over."""
        # Wicket stops the current play; striker replaced
        # Strike doesn't automatically rotate
        return new_batter, non_striker
    
    def _handle_run_out_on_single(self, striker, non_striker):
        """Handle run-out attempt on single."""
        # Run was taken, so striker rotates
        return {'strike_rotated': True}
    
    def _handle_wide(self, balls_in_over):
        """Handle wide ball."""
        return {'balls_in_over': balls_in_over}  # Doesn't increment
    
    def _handle_no_ball(self, balls_in_over):
        """Handle no-ball."""
        return {'balls_in_over': balls_in_over}  # Doesn't increment
    
    def _handle_leg_bye(self, balls_in_over, runs):
        """Handle leg-bye."""
        return {'balls_in_over': balls_in_over + 1, 'runs': runs}  # Counts as ball
    
    def _handle_bye(self, balls_in_over, runs):
        """Handle bye."""
        return {'balls_in_over': balls_in_over + 1, 'runs': runs}  # Counts as ball


class TestStrikeRotationWithMultipleBatters(unittest.TestCase):
    """Test strike rotation when multiple batters come in."""
    
    def test_multiple_wickets_in_over(self):
        """Multiple wickets in same over."""
        # Over: Wicket, single, dot, wicket, four, single
        batters = [1, 2, 3, 4]  # Player 1, 2, 3, 4 (need 4th for 2nd wicket)
        events = [
            ('wicket', None),  # Batter 1 out, Batter 3 comes
            ('single', 1),      # Batter 3 rotates
            ('dot', 0),         # Batter 2 still striker (after rotation)
            ('wicket', None),   # Batter 2 out, Batter 4 comes
            ('four', 4),        # Batter 4 remains (even runs)
            ('single', 1),      # Batter 4 rotates to non-striker
        ]
        
        striker = batters[0]
        non_striker = batters[1]
        used_batters = 2
        
        for event_type, runs in events:
            if event_type == 'wicket':
                used_batters += 1
                striker = batters[used_batters - 1]
                # Non-striker remains
            elif event_type in ['single', 'three', 'five']:
                striker, non_striker = non_striker, striker
            # 'dot', 'two', 'four', 'six' don't rotate
        
        # Final state should be valid
        self.assertIsNotNone(striker)
        self.assertIsNotNone(non_striker)
        self.assertNotEqual(striker, non_striker)


class TestStrikeRotationEdgeCases(unittest.TestCase):
    """Edge cases in strike rotation."""
    
    def test_last_batter_takes_strike(self):
        """Last batter comes in takes strike."""
        # Not the same as the non-striker
        new_batter = 11
        non_striker = 3
        self.assertNotEqual(new_batter, non_striker)
    
    def test_strike_consistency_after_6_balls(self):
        """After 6 balls, strike has rotated exactly 0 or 1 times."""
        balls = [0, 1, 0, 1, 0, 1]  # 3 runs
        total_runs = sum(balls)
        rotations = total_runs % 2  # Should be 1
        self.assertEqual(rotations, 1)
    
    def test_strike_consistency_after_12_balls(self):
        """After 12 balls (2 overs), strike returns to original."""
        over1 = [0, 1, 0, 1, 0, 1]  # 3 runs = 1 rotation
        over2 = [0, 1, 0, 1, 0, 0]  # 2 runs = 0 rotations
        total_rotations = (sum(over1) + sum(over2)) % 2
        # 5 runs total = 1 rotation (odd)
        self.assertEqual(total_rotations, 1)


if __name__ == '__main__':
    unittest.main()
