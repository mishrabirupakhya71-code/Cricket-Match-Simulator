# Cricket Logic

This guide explains how cricket rules are implemented in the simulator.

---

## 🎯 Strike Rotation

Strike rotation is one of the most important cricket mechanics. The simulator implements **exact cricket rules**.

### Rules

| Situation | Strike Rotates? | Notes |
|-----------|-----------------|-------|
| Odd runs (1, 3, 5) | ✅ Yes | Strike goes to non-striker |
| Even runs (0, 2, 4, 6) | ❌ No | Batsman continues |
| End of over | ✅ Yes | Always rotates at over end |
| Wicket | ✅ Yes | New batsman comes in |
| Bye/Leg-bye | ✅ Yes | Counts as run |
| Wide/No-ball | ❌ No | Doesn't count as ball |

### Example

**Over 1: Strike Rotation**
```
1.1 - Virat Kohli scores 1 run
     → Strike rotates to Rohit Sharma
1.2 - Rohit Sharma scores 2 runs
     → Strike stays with Rohit (even runs)
1.3 - Rohit Sharma scores 3 runs
     → Strike rotates to Virat Kohli
1.4 - Virat Kohli scores 4 runs
     → Strike stays with Virat (even runs, boundary)
1.5 - Virat Kohli is OUT
     → New batsman comes in, strike goes to Rohit
1.6 - Over ends
     → Strike rotates anyway
```

---

## 🏏 Dismissal Types

The simulator supports all **6 official cricket dismissal types**.

### 1. Bowled
- Ball hits the stumps
- Batsman doesn't touch it
- **Points: 0** (batsman)

### 2. Caught
- Ball is caught by fielder
- Can be caught off bat or glove
- **Points: 0** (batsman)

### 3. Leg Before Wicket (LBW)
- Ball hits legs and would hit stumps
- Umpire's discretion
- **Points: 0** (batsman)

### 4. Run Out
- Batsman fails to reach crease
- Can be out at either end
- **Points: 0** (batsman)

### 5. Stumped
- Similar to run out but by wicket-keeper
- Behind the crease
- **Points: 0** (batsman)

### 6. Timed Out
- Batsman takes too long (rare in modern cricket)
- **Points: 0** (batsman)

---

## 🎁 Extras

Extras are additional runs awarded without counting as a ball.

### Types of Extras

#### 1. Wide
- Ball is too wide to play
- **Awarded to** batting team
- **Counts as run** ❌ (doesn't count as ball)
- **Rotation** ❌ (no strike rotation)

```
Wide: +1 run
Ball number stays same
Batsman can't get out
```

#### 2. No-Ball
- Bowler overstepped crease
- **Awarded to** batting team
- **Counts as run** ❌ (doesn't count as ball)
- **Rotation** ❌ (no strike rotation)

```
No-ball: +1 run
Ball number stays same
Batsman can't get out (mostly)
```

#### 3. Bye
- Ball passes without touching bat
- Batsmen run between wickets
- **Counts as run & ball** ✅
- **Rotation** ✅ (based on runs)

```
1 bye: Strike rotates
2 byes: Strike stays same
```

#### 4. Leg-bye
- Ball touches body (not bat)
- Batsmen run between wickets
- **Counts as run & ball** ✅
- **Rotation** ✅ (based on runs)

```
1 leg-bye: Strike rotates
2 leg-byes: Strike stays same
```

---

## 👥 All-Out Condition

A team is all-out when the required number of batsmen have been dismissed.

### Formula

```
All-out when: (team_size - 1) wickets lost
```

### Examples

| Team Size | All-Out At | Reason |
|-----------|-----------|--------|
| **5v5** | 4 wickets | 1 batter stays in reserve |
| **8v8** | 7 wickets | 1 batter stays in reserve |
| **11v11** | 10 wickets | 1 batter stays in reserve |
| **7v7** | 6 wickets | 1 batter stays in reserve |

### Scenario

**Team India (11 batsmen):**
```
1st wicket - Virat out
2nd wicket - Rohit out
3rd wicket - Shikhar out
4th wicket - Hardik out
5th wicket - Rishabh out
6th wicket - Shreyas out
7th wicket - Jadeja out
8th wicket - Bumrah out
9th wicket - Chahal out
10th wicket - Siraj out
→ ALL OUT! (Last batter can't bat alone)
```

---

## 📊 Over Progression

### Ball Numbering

- **1 over = 6 regular balls**
- Wides and no-balls don't count
- Format: **Over.Ball** (e.g., 5.3 = 5 overs, 3 balls)

### Example Progression

```
0.1 - First ball
0.2 - Second ball
0.3 - Third ball
0.4 - Fourth ball
0.5 - Fifth ball
0.6 - Sixth ball
1.0 → (becomes 1.0 after 6 balls)
1.1 - First ball of second over
```

### With Extras

```
0.1 - Regular ball
0.2 - Wide (doesn't count)
0.2 - Replay (same number)
0.3 - Regular ball
0.4 - No-ball (doesn't count)
0.4 - Replay (same number)
0.5 - Regular ball
0.6 - Regular ball
1.0 → (becomes 1.0 - exact 6 regular balls)
```

---

## 📈 Scoring

### Runs Scoring Rules

| Delivery | Runs | Notes |
|----------|------|-------|
| Ball not hit | 0 | Dot ball |
| Ball hit, 1 run | 1 | Strike rotates |
| Ball hit, 2 runs | 2 | Strike stays |
| Ball to boundary, 4 runs | 4 | Strike stays |
| Ball over boundary, 6 runs | 6 | Strike stays |
| Wide | 1 | No rotation |
| No-ball | 1 | No rotation |
| Bye | 1-6 | Based on runs |
| Leg-bye | 1-6 | Based on runs |

### Automatic Runs

- **4 wides** in an over → automatic 4th ball called "four leg byes"
- **5 no-balls** in an over → automatic penalty

---

## 🎯 Special Cases

### Maiden Over

A maiden over is an over where **no runs are scored off the bat** (excluding wides/no-balls).

```
0.1 - Dot ball
0.2 - Dot ball
0.3 - Dot ball (wide, no-ball allowed)
0.4 - Dot ball
0.5 - Dot ball
0.6 - Dot ball
→ MAIDEN OVER!
```

### Tracking

The simulator tracks all maiden overs bowled by each bowler.

### Boundary Runs

- **4 runs** - Ball reaches boundary (not in air)
- **6 runs** - Ball goes over boundary (in air)

These trigger special awards in fantasy points.

---

## 🔢 Calculations

### Runs Per Over (RPO)

```
RPO = Total Runs / Total Overs
```

Example: 145 runs in 20 overs = 7.25 RPO

### Economy Rate (for bowlers)

```
Economy = Runs Conceded / Overs Bowled
```

Example: 35 runs in 4 overs = 8.75 economy

### Strike Rate (for batsmen)

```
Strike Rate = (Runs / Balls) × 100
```

Example: 45 runs off 32 balls = 140.6 strike rate

### Batting Average

```
Average = Total Runs / Number of Times Out
```

---

## ✅ Accuracy

This simulator implements **100% accurate** cricket logic:

✅ Proper strike rotation
✅ All dismissal types
✅ Correct extras handling
✅ Accurate maiden over detection
✅ Proper all-out conditions
✅ Correct calculations
✅ Over progression

Every rule is tested with 150+ test cases covering all scenarios.

---

## 📚 Learn More

- **[Fantasy Points System](Fantasy-Points-System)** - Points calculation
- **[Testing Guide](Testing-Guide)** - See the tests
- **[Using the Simulator](Using-the-Simulator)** - How to use it
