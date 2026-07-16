# Using the Simulator

Complete guide to using the Cricket Match Simulator.

---

## 🎮 Main Menu

When you start the application:

```
┌─────────────────────────────────────┐
│   🏏 CRICKET MATCH SIMULATOR 🏏     │
├─────────────────────────────────────┤
│  1. Create New Match                │
│  2. Resume Match                    │
│  3. Manage Players                  │
│  4. Global Rankings                 │
│  5. Recent Matches                  │
│  6. Custom SQL                      │
│  7. Exit                            │
└─────────────────────────────────────┘

Choose option:
```

---

## 1️⃣ Create New Match

### Overview
Start a brand new cricket match with custom settings.

### Steps

**1. Select "Create New Match"**
```
Choose option: 1
```

**2. Enter Match Details**
```
Enter Match Name: India vs Pakistan
Enter Total Overs: 20
Enter Team Size (number of players per team): 11
```

**3. Select Teams**
The system will show available players:
```
Select Batting Team Captain (1-10): 1
Select Bowling Team Captain (1-10): 2
```

**4. Match Starts**
The simulator begins simulating balls.

### Available Team Sizes
- **5v5** - All-out at 4 wickets
- **8v8** - All-out at 7 wickets
- **11v11** - All-out at 10 wickets
- **Any custom size** - Formula: (team_size - 1) wickets

---

## 2️⃣ Resume Match

### Overview
Continue a match you previously paused or saved.

### Steps

**1. Select "Resume Match"**
```
Choose option: 2
```

**2. Select Match to Resume**
```
Recent Matches:
1. India vs Pakistan (12/20 overs)
2. Australia vs England (8/20 overs)
3. etc...

Select match: 1
```

**3. Continue Simulation**
Match resumes from where you left off.

---

## 3️⃣ Manage Players

### Overview
Add, edit, or view players.

### Add New Player

**Steps:**
```
Choose option: 3
1. Add New Player
2. View All Players
3. Edit Player
4. Back

Choose: 1
```

**Enter Player Info:**
```
Enter Player Name: Virat Kohli
Enter Batting Average: 50.5
Enter Strike Rate: 140
Player added successfully!
```

### View All Players

```
Choose: 2
```

Shows table:
```
Player ID  Name              Avg    SR
1          Virat Kohli       50.5   140
2          MS Dhoni          50.57  145
3          AB de Villiers    54.2   150
```

### Edit Player

```
Choose: 3
Select player ID to edit: 1
Enter new average: 52.0
Player updated!
```

---

## 4️⃣ Global Rankings

### Overview
View rankings of all players across all matches.

### Steps

```
Choose option: 4
```

### Displays

**Batting Rankings**
```
Rank  Player              Matches  Runs  Avg     SR
1.    Virat Kohli         5        420   84.0    140.2
2.    MS Dhoni            5        380   76.0    142.1
3.    AB de Villiers      4        312   78.0    148.5
```

**Bowling Rankings**
```
Rank  Player              Matches  Wkts  Runs  Econ
1.    Jasprit Bumrah      5        12    85    4.2
2.    Yuzvendra Chahal    5        10    92    4.6
3.    Pat Cummins         4        9     78    4.9
```

**Fantasy Rankings**
```
Rank  Player              Total Points
1.    Virat Kohli         1250
2.    Jasprit Bumrah      985
3.    MS Dhoni            890
```

---

## 5️⃣ Recent Matches

### Overview
View past matches and their details.

### Steps

```
Choose option: 5
```

### Shows

```
Recent Matches:
1. India vs Pakistan (Completed)
   - Batting: 165/8 (20 overs)
   - Bowling: 168/5 (18.3 overs)
   - Winner: Bowling Team

2. Australia vs England (Completed)
   - Batting: 142/6 (20 overs)
   - Bowling: 145/4 (19.2 overs)
   - Winner: Bowling Team
```

### View Match Details

```
Select match: 1
```

Shows detailed statistics.

---

## 6️⃣ Custom SQL

### Overview
Advanced users can execute custom SQL queries.

### Steps

```
Choose option: 6
Enter SQL Query: SELECT * FROM players WHERE avg > 50;
```

### Examples

**Get all batsmen with average > 50**
```sql
SELECT name, avg, sr FROM players WHERE avg > 50 ORDER BY avg DESC;
```

**Get all matches**
```sql
SELECT * FROM matches;
```

**Get fantasy points for a player**
```sql
SELECT player_name, fantasy_points FROM fantasy_stats;
```

---

## 🎯 During Match Simulation

### Ball-by-Ball Display

```
Over 1.1: Virat Kohli vs Jasprit Bumrah
Runs: 4 (BOUNDARY!)
Score: India - 4/0

Over 1.2: Virat Kohli vs Jasprit Bumrah
Runs: 0 (DOT BALL)
Score: India - 4/0
```

### Controls

| Key | Action |
|-----|--------|
| **s** | Simulate next ball |
| **p** | Pause match |
| **e** | End innings |
| **q** | Quit without saving |

### Live Scorecard

```
┌──────────────────────────────┐
│  INDIA vs PAKISTAN            │
│  Innings 1 - Batting          │
├──────────────────────────────┤
│  Runs: 45/2                   │
│  Overs: 5.3                   │
│  Current Rate: 8.4            │
│                               │
│  Batsman: Virat - 18 (12)     │
│  Non-striker: Rohit - 20 (14) │
│                               │
│  Bowler: Bumrah               │
│  Extras: 2                    │
└──────────────────────────────┘
```

---

## 📊 Match Results

### Match Summary
```
Match: India vs Pakistan
Date: 2024-01-15
Batting Team: India
Bowling Team: Pakistan
Batting Score: 165/8 (20 overs)
Bowling Score: 168/5 (18.3 overs)
Winner: Pakistan
```

### Batting Statistics
```
Player         Runs  Balls  SR     4s  6s
Virat Kohli    45    32     140.6  4   2
MS Dhoni       38    28     135.7  3   1
Rohit Sharma   32    25     128.0  2   1
```

### Bowling Statistics
```
Player           Overs  Runs  Wkts  Econ
Jasprit Bumrah   4      28    2     7.0
Yuzvendra Chahal 3.2    22    1     6.6
Pat Cummins      4      35    1     8.75
```

### Fantasy Leaderboard
```
Rank  Player              Points  Source
1.    Virat Kohli         95      Batting + Bonus
2.    Jasprit Bumrah      85      Bowling + Wickets
3.    MS Dhoni            78      Batting
```

---

## 💾 Saving & Loading

### Auto-Save
- Matches are **automatically saved** after creation
- Can be resumed later with "Resume Match"

### Manual Pause
- Press **'p'** during match to pause
- Match state is saved
- Resume anytime with "Resume Match"

---

## 🎨 Interface Features

### Color-Coded Output
- 🟢 **Green** - Successful actions
- 🔴 **Red** - Errors
- 🟡 **Yellow** - Warnings
- 🔵 **Blue** - Information

### Formatted Tables
- Player statistics
- Match results
- Rankings
- Fantasy leaderboards

---

## 🆘 Tips & Tricks

✅ Add multiple players for variety
✅ Try different team sizes
✅ Check rankings after each match
✅ Use Custom SQL for advanced queries
✅ Resume matches to continue later

---

## 📚 Learn More

- **[Cricket Logic](Cricket-Logic)** - How cricket rules work
- **[Fantasy Points](Fantasy-Points-System)** - Points calculation
- **[Testing Guide](Testing-Guide)** - Run the tests
