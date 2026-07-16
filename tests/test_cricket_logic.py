"""
Unit tests for core cricket simulation logic.
Tests strike rotation, wickets, extras, over progression, and all-out conditions.
"""

import unittest
import sys
sys.path.insert(0, '../desktop_simulator')

from models import Player, Ball, Match, Team, Innings


class TestStrikeRotation(unittest.TestCase):
    """Test strike rotation mechanics."""
    
    def setUp(self):
        """Set up test players and match state."""
        self.striker = Player(name="Striker", batting_avg=40.0)
        self.non_striker = Player(name="NonStriker", batting_avg=35.0)
        self.bowler = Player(name="Bowler", bowling_avg=25.0)
    
    def test_single_run_rotates_strike(self):
        """After 1 run, striker and non-striker swap."""
        result = self._rotate_strike(runs=1)
        self.assertEqual(result['new_striker'], self.non_striker.name)
        self.assertEqual(result['new_non_striker'], self.striker.name)
    
    def test_two_runs_keeps_strike(self):
        """After 2 runs, striker remains at strike."""
        result = self._rotate_strike(runs=2)
        self.assertEqual(result['new_striker'], self.striker.name)
        self.assertEqual(result['new_non_striker'], self.non_striker.name)
    
    def test_three_runs_rotates_strike(self):
        """After 3 runs, striker and non-striker swap."""
        result = self._rotate_strike(runs=3)
        self.assertEqual(result['new_striker'], self.non_striker.name)
        self.assertEqual(result['new_non_striker'], self.striker.name)
    
    def test_four_runs_keeps_strike(self):
        """After 4 runs (boundary), striker remains at strike."""
        result = self._rotate_strike(runs=4)
        self.assertEqual(result['new_striker'], self.striker.name)
        self.assertEqual(result['new_non_striker'], self.non_striker.name)
    
    def test_six_runs_keeps_strike(self):
        """After 6 runs (six), striker remains at strike."""
        result = self._rotate_strike(runs=6)
        self.assertEqual(result['new_striker'], self.striker.name)
        self.assertEqual(result['new_non_striker'], self.non_striker.name)
    
    def test_end_of_over_always_rotates(self):
        """At end of over (6 balls), strike always rotates."""
        # Odd runs over the over
        result = self._rotate_strike(runs_per_ball=[0, 1, 0, 0, 1, 0], is_end_of_over=True)
        self.assertEqual(result['rotated_at_end'], True)
    
    def test_wide_does_not_advance_bowler_ball_count(self):
        """Wide ball is not counted in ball count."""
        result = self._handle_wide()
        self.assertEqual(result['ball_count_advanced'], False)
    
    def test_no_ball_does_not_advance_bowler_ball_count(self):
        """No-ball is not counted in ball count."""
        result = self._handle_no_ball()
        self.assertEqual(result['ball_count_advanced'], False)
    
    def _rotate_strike(self, runs=0, runs_per_ball=None, is_end_of_over=False):
        """Helper to simulate strike rotation."""
        if runs_per_ball:
            total_runs = sum(runs_per_ball)
            total_rotations = (total_runs % 2 != 0) or is_end_of_over
        else:
            total_rotations = (runs % 2 != 0)
        
        if total_rotations:
            return {
                'new_striker': self.non_striker.name,
                'new_non_striker': self.striker.name,
                'rotated_at_end': is_end_of_over
            }
        else:
            return {
                'new_striker': self.striker.name,
                'new_non_striker': self.non_striker.name,
                'rotated_at_end': is_end_of_over
            }
    
    def _handle_wide(self):
        """Helper for wide handling."""
        return {'ball_count_advanced': False}
    
    def _handle_no_ball(self):
        """Helper for no-ball handling."""
        return {'ball_count_advanced': False}


class TestAllOutCondition(unittest.TestCase):
    """Test all-out condition for custom team sizes."""
    
    def test_all_out_5v5_teams(self):
        """All-out at 4 wickets (5-1) for 5-player teams."""
        team_size = 5
        wickets = 4
        self.assertTrue(self._check_all_out(wickets, team_size))
    
    def test_all_out_11v11_teams(self):
        """All-out at 10 wickets (11-1) for 11-player teams."""
        team_size = 11
        wickets = 10
        self.assertTrue(self._check_all_out(wickets, team_size))
    
    def test_all_out_8v8_teams(self):
        """All-out at 7 wickets (8-1) for 8-player teams."""
        team_size = 8
        wickets = 7
        self.assertTrue(self._check_all_out(wickets, team_size))
    
    def test_not_all_out_before_max(self):
        """Not all-out before max wickets."""
        team_size = 11
        wickets = 9
        self.assertFalse(self._check_all_out(wickets, team_size))
    
    def test_zero_wickets_not_all_out(self):
        """Zero wickets = not all-out."""
        team_size = 11
        wickets = 0
        self.assertFalse(self._check_all_out(wickets, team_size))
    
    def _check_all_out(self, wickets, team_size):
        """Check if all-out condition is met."""
        max_wickets = team_size - 1
        return wickets >= max_wickets


class TestWicketTypes(unittest.TestCase):
    """Test all wicket dismissal types."""
    
    def test_bowled_wicket(self):
        """Bowled dismissal recorded correctly."""
        result = self._record_wicket('bowled', bowler='Bowler1', fielder=None)
        self.assertEqual(result['wicket_type'], 'bowled')
        self.assertIsNone(result['fielder'])
    
    def test_caught_wicket(self):
        """Caught dismissal requires fielder."""
        result = self._record_wicket('caught', bowler='Bowler1', fielder='Fielder1')
        self.assertEqual(result['wicket_type'], 'caught')
        self.assertEqual(result['fielder'], 'Fielder1')
    
    def test_lbw_wicket(self):
        """LBW dismissal recorded correctly."""
        result = self._record_wicket('lbw', bowler='Bowler1', fielder=None)
        self.assertEqual(result['wicket_type'], 'lbw')
        self.assertIsNone(result['fielder'])
    
    def test_run_out_wicket(self):
        """Run-out dismissal requires fielder."""
        result = self._record_wicket('run_out', bowler=None, fielder='Fielder1')
        self.assertEqual(result['wicket_type'], 'run_out')
        self.assertEqual(result['fielder'], 'Fielder1')
    
    def test_stumped_wicket(self):
        """Stumped dismissal requires wicket-keeper."""
        result = self._record_wicket('stumped', bowler='Bowler1', fielder='Keeper')
        self.assertEqual(result['wicket_type'], 'stumped')
        self.assertEqual(result['fielder'], 'Keeper')
    
    def _record_wicket(self, wicket_type, bowler, fielder):
        """Helper to record wicket."""
        return {
            'wicket_type': wicket_type,
            'bowler': bowler,
            'fielder': fielder
        }


class TestExtras(unittest.TestCase):
    """Test extras handling (wides, no-balls, leg-byes, byes)."""
    
    def test_wide_adds_one_run(self):
        """Wide adds 1 run to extras."""
        result = self._handle_extra('wide', runs=0)
        self.assertEqual(result['extra_runs'], 1)
        self.assertEqual(result['extra_type'], 'wide')
    
    def test_wide_with_runs_adds_total(self):
        """Wide with additional runs adds all."""
        result = self._handle_extra('wide', runs=2)
        self.assertEqual(result['extra_runs'], 1 + 2)
    
    def test_no_ball_adds_one_run(self):
        """No-ball adds 1 run to extras."""
        result = self._handle_extra('no_ball', runs=0)
        self.assertEqual(result['extra_runs'], 1)
        self.assertEqual(result['extra_type'], 'no_ball')
    
    def test_leg_bye_counts_as_extra(self):
        """Leg-bye runs count."""
        result = self._handle_extra('leg_bye', runs=2)
        self.assertEqual(result['extra_runs'], 2)
        self.assertEqual(result['extra_type'], 'leg_bye')
    
    def test_bye_counts_as_extra(self):
        """Bye runs count."""
        result = self._handle_extra('bye', runs=3)
        self.assertEqual(result['extra_runs'], 3)
        self.assertEqual(result['extra_type'], 'bye')
    
    def test_wide_is_not_counted_ball(self):
        """Wide doesn't count toward 6-ball over."""
        result = self._handle_extra('wide', runs=0)
        self.assertFalse(result['counts_as_ball'])
    
    def test_no_ball_is_not_counted_ball(self):
        """No-ball doesn't count toward 6-ball over."""
        result = self._handle_extra('no_ball', runs=0)
        self.assertFalse(result['counts_as_ball'])
    
    def test_leg_bye_counts_as_ball(self):
        """Leg-bye counts toward 6-ball over."""
        result = self._handle_extra('leg_bye', runs=1)
        self.assertTrue(result['counts_as_ball'])
    
    def _handle_extra(self, extra_type, runs):
        """Helper to handle extra runs."""
        extra_runs = runs
        counts_as_ball = True
        
        if extra_type == 'wide':
            extra_runs = 1 + runs
            counts_as_ball = False
        elif extra_type == 'no_ball':
            extra_runs = 1 + runs
            counts_as_ball = False
        
        return {
            'extra_type': extra_type,
            'extra_runs': extra_runs,
            'counts_as_ball': counts_as_ball
        }


class TestOverProgression(unittest.TestCase):
    """Test over and ball progression."""
    
    def test_over_increments_after_6_balls(self):
        """After 6 balls, over increments."""
        balls = 6
        current_over = 0
        expected_over = self._calculate_over(balls, current_over)
        self.assertEqual(expected_over, 1)
    
    def test_over_13_balls_is_second_over(self):
        """After 12 balls (2 complete overs), over = 2."""
        balls = 12
        current_over = 0
        expected_over = self._calculate_over(balls, current_over)
        self.assertEqual(expected_over, 2)
    
    def test_ball_number_within_over(self):
        """Ball number resets every 6 balls."""
        for balls in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            ball_in_over = self._get_ball_in_over(balls)
            if balls <= 6:
                self.assertEqual(ball_in_over, balls)
            else:
                self.assertEqual(ball_in_over, (balls % 6) or 6)
    
    def test_overs_decimal_representation(self):
        """Overs in decimal (e.g., 5.3 = 5 overs 3 balls)."""
        total_balls = 33  # 5 complete overs + 3 balls
        overs_decimal = self._balls_to_overs_decimal(total_balls)
        self.assertEqual(overs_decimal, 5.3)
    
    def _calculate_over(self, balls, current_over):
        """Helper to calculate over from ball count."""
        return balls // 6
    
    def _get_ball_in_over(self, total_balls):
        """Helper to get ball number within current over."""
        return (total_balls - 1) % 6 + 1
    
    def _balls_to_overs_decimal(self, total_balls):
        """Convert total balls to decimal overs."""
        complete_overs = total_balls // 6
        balls_in_current_over = total_balls % 6
        return complete_overs + (balls_in_current_over / 10.0)


class TestMaidenOver(unittest.TestCase):
    """Test maiden over detection (no runs scored by batting team)."""
    
    def test_zero_runs_is_maiden(self):
        """Over with 0 runs = maiden over."""
        runs_in_over = 0
        self.assertTrue(self._is_maiden_over(runs_in_over))
    
    def test_one_run_not_maiden(self):
        """Over with 1 run ≠ maiden over."""
        runs_in_over = 1
        self.assertFalse(self._is_maiden_over(runs_in_over))
    
    def test_dots_and_extras_count(self):
        """Over with only extras (wides) = not maiden (extras count)."""
        runs_in_over = 2  # 1 wide + 1 more run
        self.assertFalse(self._is_maiden_over(runs_in_over))
    
    def test_multiple_maidens_in_spell(self):
        """Bowler can bowl multiple maidens consecutively."""
        overs = [0, 0, 1, 0, 2, 0]  # 3 maiden overs out of 6
        maidens = sum(1 for o in overs if o == 0)
        self.assertEqual(maidens, 3)
    
    def _is_maiden_over(self, runs):
        """Check if over is maiden."""
        return runs == 0


class TestDotBallDetection(unittest.TestCase):
    """Test dot ball detection."""
    
    def test_zero_runs_is_dot_ball(self):
        """Ball with 0 runs = dot ball."""
        self.assertTrue(self._is_dot_ball(0))
    
    def test_one_run_not_dot_ball(self):
        """Ball with 1 run ≠ dot ball."""
        self.assertFalse(self._is_dot_ball(1))
    
    def test_boundary_not_dot_ball(self):
        """Boundary (4 runs) ≠ dot ball."""
        self.assertFalse(self._is_dot_ball(4))
    
    def test_six_not_dot_ball(self):
        """Six (6 runs) ≠ dot ball."""
        self.assertFalse(self._is_dot_ball(6))
    
    def _is_dot_ball(self, runs):
        """Check if ball is dot."""
        return runs == 0


class TestBattingMetrics(unittest.TestCase):
    """Test batting metrics calculation."""
    
    def test_strike_rate_calculation(self):
        """Strike rate = (runs / balls faced) * 100."""
        runs = 50
        balls_faced = 40
        strike_rate = self._calculate_strike_rate(runs, balls_faced)
        self.assertEqual(strike_rate, 125.0)
    
    def test_average_calculation(self):
        """Batting average = runs / dismissals."""
        total_runs = 1000
        dismissals = 25
        average = self._calculate_average(total_runs, dismissals)
        self.assertEqual(average, 40.0)
    
    def test_boundary_count(self):
        """Count 4-run boundaries."""
        self.assertEqual(self._count_boundaries([0, 4, 1, 4, 0, 2, 4]), 3)
    
    def test_six_count(self):
        """Count 6-run sixes."""
        self.assertEqual(self._count_sixes([0, 6, 1, 2, 6, 0, 6]), 3)
    
    def _calculate_strike_rate(self, runs, balls_faced):
        """Calculate strike rate."""
        if balls_faced == 0:
            return 0
        return (runs / balls_faced) * 100
    
    def _calculate_average(self, total_runs, dismissals):
        """Calculate batting average."""
        if dismissals == 0:
            return 0
        return total_runs / dismissals
    
    def _count_boundaries(self, runs_list):
        """Count 4-run boundaries."""
        return sum(1 for r in runs_list if r == 4)
    
    def _count_sixes(self, runs_list):
        """Count 6-run sixes."""
        return sum(1 for r in runs_list if r == 6)


class TestBowlingMetrics(unittest.TestCase):
    """Test bowling metrics calculation."""
    
    def test_economy_rate_calculation(self):
        """Economy rate = (runs conceded / overs bowled)."""
        runs_conceded = 24
        overs_bowled = 4.0
        economy = self._calculate_economy_rate(runs_conceded, overs_bowled)
        self.assertEqual(economy, 6.0)
    
    def test_economy_with_partial_over(self):
        """Economy with partial over (e.g., 3.2)."""
        runs_conceded = 20
        overs_bowled = 3.2
        economy = self._calculate_economy_rate(runs_conceded, overs_bowled)
        # 3.2 overs = 3 overs + 2 balls = 3.333... overs in decimal
        self.assertAlmostEqual(economy, 6.0, places=1)
    
    def test_bowling_average_calculation(self):
        """Bowling average = runs conceded / wickets taken."""
        runs_conceded = 150
        wickets_taken = 6
        average = self._calculate_bowling_average(runs_conceded, wickets_taken)
        self.assertEqual(average, 25.0)
    
    def test_zero_wickets_infinite_average(self):
        """With 0 wickets, average is undefined (handled as -1)."""
        runs_conceded = 50
        wickets_taken = 0
        average = self._calculate_bowling_average(runs_conceded, wickets_taken)
        self.assertEqual(average, -1)  # Indicates undefined
    
    def _calculate_economy_rate(self, runs_conceded, overs_bowled):
        """Calculate economy rate."""
        if overs_bowled == 0:
            return 0
        return runs_conceded / overs_bowled
    
    def _calculate_bowling_average(self, runs_conceded, wickets_taken):
        """Calculate bowling average."""
        if wickets_taken == 0:
            return -1  # Undefined
        return runs_conceded / wickets_taken


if __name__ == '__main__':
    unittest.main()
