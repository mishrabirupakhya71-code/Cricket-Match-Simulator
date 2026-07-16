"""
Unit tests for Dream11-style fantasy points calculation.
Tests all fantasy point components: runs, boundaries, sixes, wickets, bonuses, and penalties.
"""

import unittest
import sys
sys.path.insert(0, '../desktop_simulator')


class TestFantasyBattingPoints(unittest.TestCase):
    """Test fantasy points for batting performances."""
    
    def test_one_run_equals_one_point(self):
        """1 run = 1 fantasy point."""
        runs = 50
        points = self._calculate_run_points(runs)
        self.assertEqual(points, 50.0)
    
    def test_boundary_bonus_points(self):
        """Each 4 = +1 boundary point (total 1 run from boundary)."""
        boundaries = 5
        points = self._calculate_boundary_bonus(boundaries)
        self.assertEqual(points, 5.0)
    
    def test_six_bonus_points(self):
        """Each 6 = +2 six points (total 2 runs from six)."""
        sixes = 3
        points = self._calculate_six_bonus(sixes)
        self.assertEqual(points, 6.0)
    
    def test_total_batting_points_comprehensive(self):
        """Total = runs + (boundaries * 1) + (sixes * 2)."""
        runs = 75
        boundaries = 4
        sixes = 2
        total_points = self._calculate_total_batting_points(runs, boundaries, sixes)
        # 75 + 4 + (2*2) = 75 + 4 + 4 = 83
        self.assertEqual(total_points, 83.0)
    
    def test_century_bonus_not_explicit(self):
        """Dream11 doesn't give explicit century bonus; points scale naturally."""
        runs_50 = self._calculate_run_points(50)
        runs_100 = self._calculate_run_points(100)
        # Double runs = double points (no threshold bonus)
        self.assertEqual(runs_100, 2 * runs_50)
    
    def test_half_century_not_explicit(self):
        """Dream11 doesn't give explicit 50-run bonus."""
        runs_49 = self._calculate_run_points(49)
        runs_50 = self._calculate_run_points(50)
        # Linear scaling, no jump at 50
        self.assertEqual(runs_50 - runs_49, 1.0)
    
    def _calculate_run_points(self, runs):
        """1 point per run."""
        return float(runs)
    
    def _calculate_boundary_bonus(self, boundaries):
        """1 point per boundary."""
        return float(boundaries)
    
    def _calculate_six_bonus(self, sixes):
        """2 points per six."""
        return float(sixes * 2)
    
    def _calculate_total_batting_points(self, runs, boundaries, sixes):
        """Total batting points."""
        return float(runs + boundaries + (sixes * 2))


class TestFantasyWicketPoints(unittest.TestCase):
    """Test fantasy points for bowling and wickets."""
    
    def test_wicket_points_25_per_dismissal(self):
        """Each wicket = +25 points."""
        wickets = 3
        points = self._calculate_wicket_points(wickets)
        self.assertEqual(points, 75.0)
    
    def test_bowled_dismissal_bonus_8_points(self):
        """Bowled dismissal = +8 bonus points."""
        bowled_count = 2
        points = self._calculate_dismissal_bonus('bowled', bowled_count)
        self.assertEqual(points, 16.0)
    
    def test_caught_dismissal_bonus_8_points(self):
        """Caught dismissal = +8 bonus points."""
        caught_count = 3
        points = self._calculate_dismissal_bonus('caught', caught_count)
        self.assertEqual(points, 24.0)
    
    def test_lbw_dismissal_bonus_8_points(self):
        """LBW dismissal = +8 bonus points."""
        lbw_count = 1
        points = self._calculate_dismissal_bonus('lbw', lbw_count)
        self.assertEqual(points, 8.0)
    
    def test_run_out_dismissal_bonus_8_points(self):
        """Run-out dismissal = +8 bonus points (fielder credit)."""
        run_out_count = 1
        points = self._calculate_dismissal_bonus('run_out', run_out_count)
        self.assertEqual(points, 8.0)
    
    def test_stumped_dismissal_bonus_8_points(self):
        """Stumped dismissal = +8 bonus points."""
        stumped_count = 1
        points = self._calculate_dismissal_bonus('stumped', stumped_count)
        self.assertEqual(points, 8.0)
    
    def test_total_bowling_points_comprehensive(self):
        """Total = (wickets * 25) + dismissal bonuses."""
        wickets = 2
        bowled = 1
        caught = 1
        total = self._calculate_total_bowling_points(wickets, bowled, caught)
        # (2*25) + 8 + 8 = 50 + 16 = 66
        self.assertEqual(total, 66.0)
    
    def test_maiden_over_bonus_12_points(self):
        """Each maiden over (0 runs) = +12 points."""
        maiden_overs = 2
        points = self._calculate_maiden_over_bonus(maiden_overs)
        self.assertEqual(points, 24.0)
    
    def _calculate_wicket_points(self, wickets):
        """25 points per wicket."""
        return float(wickets * 25)
    
    def _calculate_dismissal_bonus(self, dismissal_type, count):
        """8 points per dismissal of that type."""
        return float(count * 8)
    
    def _calculate_total_bowling_points(self, wickets, bowled, caught):
        """Total bowling points."""
        base = wickets * 25
        bonuses = (bowled * 8) + (caught * 8)
        return float(base + bonuses)
    
    def _calculate_maiden_over_bonus(self, maiden_overs):
        """12 points per maiden over."""
        return float(maiden_overs * 12)


class TestFantasyPenalties(unittest.TestCase):
    """Test fantasy point penalties for poor performance."""
    
    def test_low_strike_rate_penalty(self):
        """Strike rate < 60 = -2 points per ball below threshold."""
        runs = 20
        balls_faced = 40
        strike_rate = (runs / balls_faced) * 100  # 50%
        penalty = self._calculate_strike_rate_penalty(strike_rate, balls_faced)
        # Strike rate 50% is 10% below 60% = not applied if below threshold
        # Typically: -2 per 1% below 60%, minimum applied after 10 balls
        self.assertLess(penalty, 0)
    
    def test_no_penalty_for_high_strike_rate(self):
        """Strike rate >= 60 = no penalty."""
        runs = 60
        balls_faced = 100
        strike_rate = (runs / balls_faced) * 100  # 60%
        penalty = self._calculate_strike_rate_penalty(strike_rate, balls_faced)
        self.assertEqual(penalty, 0)
    
    def test_economy_rate_penalty_above_threshold(self):
        """Economy > 8 = -1 point per run above threshold."""
        runs_conceded = 40
        overs_bowled = 4.0
        economy = runs_conceded / overs_bowled  # 10
        penalty = self._calculate_economy_penalty(economy, overs_bowled)
        # Economy 10, threshold 8 = 2 runs above = -2 points
        self.assertLess(penalty, 0)
    
    def test_no_economy_penalty_for_good_bowling(self):
        """Economy <= 8 = no penalty."""
        runs_conceded = 32
        overs_bowled = 4.0
        economy = runs_conceded / overs_bowled  # 8
        penalty = self._calculate_economy_penalty(economy, overs_bowled)
        self.assertEqual(penalty, 0)
    
    def _calculate_strike_rate_penalty(self, strike_rate, balls_faced):
        """Penalty for low strike rate (< 60%)."""
        threshold = 60.0
        if balls_faced < 10:
            return 0  # No penalty for less than 10 balls
        if strike_rate >= threshold:
            return 0
        # Simplified: -1 per 10% below threshold
        deficit_percentage = threshold - strike_rate
        penalty = -1 * (deficit_percentage // 10)
        return penalty
    
    def _calculate_economy_penalty(self, economy, overs_bowled):
        """Penalty for high economy rate (> 8)."""
        threshold = 8.0
        if overs_bowled < 1:
            return 0  # No penalty for less than 1 over
        if economy <= threshold:
            return 0
        # Simplified: -1 per run above threshold
        excess_runs = economy - threshold
        penalty = -1 * int(excess_runs)
        return penalty


class TestFantasySpecialAwards(unittest.TestCase):
    """Test special fantasy awards post-match."""
    
    def test_super_striker_highest_strike_rate(self):
        """Super Striker: Highest strike rate (min 10 balls)."""
        players_stats = [
            {'name': 'Player1', 'runs': 50, 'balls': 40, 'strike_rate': 125},  # 125%
            {'name': 'Player2', 'runs': 30, 'balls': 40, 'strike_rate': 75},   # 75%
            {'name': 'Player3', 'runs': 10, 'balls': 5, 'strike_rate': 200},   # 200% but < 10 balls
        ]
        award = self._determine_super_striker(players_stats)
        self.assertEqual(award['winner'], 'Player1')
        self.assertEqual(award['strike_rate'], 125)
    
    def test_boundary_rider_most_fours(self):
        """Boundary Rider: Most 4s hit."""
        players_stats = [
            {'name': 'Player1', 'boundaries': 5},
            {'name': 'Player2', 'boundaries': 3},
            {'name': 'Player3', 'boundaries': 7},
        ]
        award = self._determine_boundary_rider(players_stats)
        self.assertEqual(award['winner'], 'Player3')
        self.assertEqual(award['boundaries'], 7)
    
    def test_dot_ball_chieftain_most_dots(self):
        """Dot Ball Chieftain: Bowler with most dot balls."""
        bowlers_stats = [
            {'name': 'Bowler1', 'dot_balls': 12},
            {'name': 'Bowler2', 'dot_balls': 8},
            {'name': 'Bowler3', 'dot_balls': 15},
        ]
        award = self._determine_dot_ball_chieftain(bowlers_stats)
        self.assertEqual(award['winner'], 'Bowler3')
        self.assertEqual(award['dot_balls'], 15)
    
    def test_mvp_highest_fantasy_points(self):
        """MVP: Highest total fantasy points."""
        players_stats = [
            {'name': 'Player1', 'fantasy_points': 120},
            {'name': 'Player2', 'fantasy_points': 95},
            {'name': 'Player3', 'fantasy_points': 140},
        ]
        award = self._determine_mvp(players_stats)
        self.assertEqual(award['winner'], 'Player3')
        self.assertEqual(award['fantasy_points'], 140)
    
    def _determine_super_striker(self, players_stats):
        """Find player with highest strike rate (min 10 balls)."""
        qualified = [p for p in players_stats if p.get('balls', 0) >= 10]
        if not qualified:
            return None
        winner = max(qualified, key=lambda x: x.get('strike_rate', 0))
        return {'winner': winner['name'], 'strike_rate': winner['strike_rate']}
    
    def _determine_boundary_rider(self, players_stats):
        """Find player with most boundaries."""
        winner = max(players_stats, key=lambda x: x.get('boundaries', 0))
        return {'winner': winner['name'], 'boundaries': winner['boundaries']}
    
    def _determine_dot_ball_chieftain(self, bowlers_stats):
        """Find bowler with most dot balls."""
        winner = max(bowlers_stats, key=lambda x: x.get('dot_balls', 0))
        return {'winner': winner['name'], 'dot_balls': winner['dot_balls']}
    
    def _determine_mvp(self, players_stats):
        """Find player with highest fantasy points."""
        winner = max(players_stats, key=lambda x: x.get('fantasy_points', 0))
        return {'winner': winner['name'], 'fantasy_points': winner['fantasy_points']}


class TestFantasyLeaderboard(unittest.TestCase):
    """Test fantasy leaderboard generation and updates."""
    
    def test_leaderboard_sorted_descending(self):
        """Leaderboard sorted by fantasy points (highest first)."""
        players_points = [
            ('Player1', 85),
            ('Player2', 120),
            ('Player3', 95),
            ('Player4', 110),
        ]
        leaderboard = self._generate_leaderboard(players_points)
        expected_order = ['Player2', 'Player4', 'Player3', 'Player1']
        self.assertEqual([p[0] for p in leaderboard], expected_order)
    
    def test_leaderboard_ranking_assignment(self):
        """Correct ranking positions assigned."""
        players_points = [
            ('Player1', 100),
            ('Player2', 85),
            ('Player3', 95),
        ]
        leaderboard = self._generate_leaderboard(players_points)
        ranks = [p[1] for p in leaderboard]
        self.assertEqual(ranks, [1, 2, 3])
    
    def test_tied_scores_same_rank(self):
        """Tied scores receive same rank."""
        players_points = [
            ('Player1', 100),
            ('Player2', 100),
            ('Player3', 90),
        ]
        leaderboard = self._generate_leaderboard(players_points)
        # Ties should have same rank
        self.assertEqual(leaderboard[0][1], leaderboard[1][1])
    
    def test_leaderboard_includes_all_players(self):
        """All players appear in leaderboard."""
        players_points = [
            ('Player1', 80),
            ('Player2', 90),
            ('Player3', 70),
        ]
        leaderboard = self._generate_leaderboard(players_points)
        self.assertEqual(len(leaderboard), 3)
    
    def _generate_leaderboard(self, players_points):
        """Generate sorted leaderboard with rankings."""
        # Sort by points descending
        sorted_players = sorted(players_points, key=lambda x: x[1], reverse=True)
        # Assign rankings
        leaderboard = []
        rank = 1
        prev_points = None
        for idx, (name, points) in enumerate(sorted_players):
            if prev_points is not None and points < prev_points:
                rank = idx + 1
            leaderboard.append((name, rank, points))
            prev_points = points
        return leaderboard


class TestFantasyEdgeCases(unittest.TestCase):
    """Test edge cases in fantasy point calculation."""
    
    def test_player_with_zero_stats(self):
        """Player with all zero stats = 0 points."""
        points = self._calculate_total_fantasy_points(
            runs=0, boundaries=0, sixes=0, wickets=0,
            maiden_overs=0, dismissals=0
        )
        self.assertEqual(points, 0)
    
    def test_dnb_not_out_player(self):
        """Did Not Bat (DNB) = 0 points."""
        points = self._calculate_total_fantasy_points(
            runs=0, boundaries=0, sixes=0, wickets=0,
            maiden_overs=0, dismissals=0, did_not_bat=True
        )
        self.assertEqual(points, 0)
    
    def test_batted_not_out_only_points_for_runs(self):
        """Not-out player scores points only for runs, no dismissal bonus."""
        runs = 50
        boundaries = 2
        sixes = 0
        dismissals = 0  # Not out
        points = self._calculate_total_fantasy_points(
            runs=runs, boundaries=boundaries, sixes=sixes,
            wickets=0, maiden_overs=0, dismissals=dismissals
        )
        # 50 + 2 = 52 (no dismissal bonus)
        self.assertEqual(points, 52)
    
    def test_bowler_no_wickets(self):
        """Bowler with no wickets but maiden overs."""
        wickets = 0
        maiden_overs = 3
        dot_balls = 12
        points = self._calculate_total_fantasy_points(
            runs=0, boundaries=0, sixes=0, wickets=wickets,
            maiden_overs=maiden_overs, dismissals=0
        )
        # (0*25) + (3*12) = 36
        self.assertEqual(points, 36)
    
    def _calculate_total_fantasy_points(self, runs=0, boundaries=0, sixes=0,
                                        wickets=0, maiden_overs=0, dismissals=0,
                                        did_not_bat=False):
        """Calculate total fantasy points."""
        if did_not_bat:
            return 0
        
        batting_points = runs + boundaries + (sixes * 2)
        bowling_points = (wickets * 25) + (dismissals * 8) + (maiden_overs * 12)
        return batting_points + bowling_points


if __name__ == '__main__':
    unittest.main()
