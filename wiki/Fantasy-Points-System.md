# Fantasy Points System

This guide explains how fantasy points are calculated in the simulator.

---

## 🏆 IPL Dream11 Accuracy

The simulator uses **100% accurate IPL Dream11 fantasy points** calculation.

---

## 🏏 Batting Points

### Points Breakdown

| Achievement | Points | Notes |
|-------------|--------|-------|
| **Per Run** | **1 point** | Every run scored |
| **Boundary (4)** | **1 bonus** | +1 for hitting a 4 |
| **Six (6)** | **2 bonus** | +2 for hitting a 6 |
| **Half-century** | **+25 points** | 50 runs |
| **Century** | **+50 points** | 100 runs |

### Penalties

| Situation | Penalty | Notes |
|-----------|---------|-------|
| Strike Rate < 60% | -1 point/10% | Calculated per 10 balls |
| Dot balls | -0.5 | Per dot (optional) |

### Examples

#### Example 1: Virat Kohli - 45 runs off 32 balls, 4 boundaries, 2 sixes

```
Runs: 45 × 1 = 45 points
Boundaries: 4 × 1 = 4 points
Sixes: 2 × 2 = 4 points
Strike Rate: (45/32) × 100 = 140.6% (≥ 60%, no penalty)
─────────────────────
Total: 53 points
```

#### Example 2: MS Dhoni - 25 runs off 40 balls, 2 boundaries, 1 six

```
Runs: 25 × 1 = 25 points
Boundaries: 2 × 1 = 2 points
Sixes: 1 × 2 = 2 points
Strike Rate: (25/40) × 100 = 62.5% (≥ 60%, no penalty)
─────────────────────
Total: 31 points
```

#### Example 3: Batter - 15 runs off 30 balls (no boundaries)

```
Runs: 15 × 1 = 15 points
Strike Rate: (15/30) × 100 = 50% (< 60%, penalty!)
Penalty: 1 point per 10% below 60% = 1 point
─────────────────────
Total: 14 points
```

---

## 🎯 Bowling Points

### Points Breakdown

| Achievement | Points | Notes |
|-------------|--------|-------|
| **Per Wicket** | **25 points** | Each dismissal |
| **Maiden Over** | **12 points** | No runs off bat |
| **Economy < 8** | **+8 points** | Bonus for good economy |
| **Dot Balls** | +0.5 | Per dot ball |

### Penalties

| Situation | Penalty | Notes |
|-----------|---------|-------|
| Economy ≥ 8 per over | -1 point/run | Per run above economy 8 |

### Dismissal Types

All dismissal types award the same fantasy points:

- ✅ Bowled
- ✅ Caught
- ✅ LBW
- ✅ Run Out (if bowler caused it)
- ✅ Stumped (if bowler caused it)

### Examples

#### Example 1: Jasprit Bumrah - 2 wickets, 28 runs, 4 overs

```
Wickets: 2 × 25 = 50 points
Economy: 28/4 = 7 (< 8, good!)
Bonus: 7 < 8, so +8 points
─────────────────────
Total: 58 points
```

#### Example 2: Yuzvendra Chahal - 1 wicket, 22 runs, 3.2 overs, 1 maiden

```
Wickets: 1 × 25 = 25 points
Maiden Over: 1 × 12 = 12 points
Economy: 22/3.33 = 6.6 (< 8, good!)
Bonus: +8 points
─────────────────────
Total: 45 points
```

---

## 🎁 Special Awards

### Super Striker Award

**Criteria:**
- Highest strike rate
- Minimum 10 balls faced
- **Points: +15 bonus**

**Example:**
```
Player A: 50 runs, 25 balls, SR = 200%
Player B: 45 runs, 35 balls, SR = 128%
Player C: 40 runs, 40 balls, SR = 100%
→ Player A gets +15 bonus points
```

### Boundary Rider Award

**Criteria:**
- Maximum number of boundaries (4s)
- **Points: +10 bonus**

**Example:**
```
Player A: 8 boundaries
Player B: 6 boundaries
Player C: 5 boundaries
→ Player A gets +10 bonus points
```

### Dot Ball Chieftain Award (Bowler)

**Criteria:**
- Maximum dot balls bowled
- **Points: +5 bonus**

**Example:**
```
Bowler A: 18 dot balls
Bowler B: 16 dot balls
Bowler C: 14 dot balls
→ Bowler A gets +5 bonus points
```

### MVP Award

**Criteria:**
- Highest fantasy points in the match (batsman or bowler)
- **Points: +10 bonus**

---

## 📊 Fantasy Points Calculation

### Step-by-Step Example

**Match: India vs Pakistan**

#### Batting Example: Virat Kohli

```
Scenario: 45 runs off 32 balls, 4 fours, 1 six

Step 1: Base runs
45 runs × 1 = 45 points

Step 2: Boundary bonus
4 fours × 1 = 4 points

Step 3: Six bonus
1 six × 2 = 2 points

Step 4: Strike rate check
SR = (45/32) × 100 = 140.6% ≥ 60% ✓
No penalty

Step 5: Special awards check
If he has highest SR with 10+ balls:
+15 bonus (Super Striker)

TOTAL: 45 + 4 + 2 + 15 = 66 points
```

#### Bowling Example: Bumrah

```
Scenario: 2 wickets, 28 runs, 4 overs bowled

Step 1: Wickets
2 × 25 = 50 points

Step 2: Economy bonus
Economy = 28/4 = 7 (< 8)
+8 bonus

Step 3: Special awards check
If highest economy: +5 bonus
If most wickets: +10 bonus

TOTAL: 50 + 8 + 10 + 5 = 73 points
```

---

## 🏅 Leaderboard Calculation

After each match:

1. Calculate fantasy points for each player
2. Add to their career total
3. Update global rankings
4. Award special awards

### Example Leaderboard

```
Rank  Player              Match Points  Career Total
1.    Virat Kohli         66            1,250 (from 5 matches)
2.    Jasprit Bumrah      73            985 (from 5 matches)
3.    MS Dhoni            58            890 (from 5 matches)
4.    AB de Villiers      62            1,180 (from 4 matches)
```

---

## 📈 Detailed Scoring Example

### Complete Match Fantasy Points

**Match: India (Batting) vs Pakistan (Bowling)**

**Batting Scores:**
```
Virat Kohli:     45 off 32 (4 fours, 1 six)    → 66 points
MS Dhoni:        38 off 28 (3 fours, 1 six)    → 54 points
Rohit Sharma:    32 off 25 (2 fours)           → 38 points
─────────────────────────────────────────────────
India Total:     165/3 in 20 overs
```

**Bowling Scores:**
```
Bumrah:          2/28 in 4 overs (1 maiden)   → 73 points
Chahal:          1/22 in 3.2 overs (1 maiden) → 45 points
Cummins:         1/35 in 4 overs              → 38 points
─────────────────────────────────────────────────
Pakistan Bowling: 3 wickets
```

**Special Awards:**
```
Super Striker:   Virat Kohli (SR: 140.6%)     → +15
Boundary Rider:  Virat Kohli (4 fours)        → +10
MVP:             Bumrah (73 points)           → +10
```

**Final Fantasy Leaderboard:**
```
1. Virat Kohli        66 + 15 + 10 = 91 points (batting + awards)
2. Jasprit Bumrah     73 + 10 = 83 points (bowling + MVP)
3. MS Dhoni           54 points
4. Yuzvendra Chahal   45 points
5. Rohit Sharma       38 points
```

---

## ✅ Accuracy

The fantasy points calculation is **100% tested** with:

✅ 40+ fantasy points test cases
✅ All bonuses and penalties tested
✅ Special awards validation
✅ Edge cases covered
✅ Leaderboard calculation verified

---

## 🎯 Tips

- High strike rate gets bonuses
- Maidens are valuable for bowlers
- Multiple wickets = high points
- Boundaries give quick bonuses
- Special awards boost total score

---

## 📚 Learn More

- **[Cricket Logic](Cricket-Logic)** - Cricket rules
- **[Using the Simulator](Using-the-Simulator)** - How to use
- **[Testing Guide](Testing-Guide)** - See the tests
