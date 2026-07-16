# Quick Start Guide

Get the Cricket Match Simulator running in **5 minutes**!

---

## ⚡ Super Quick Setup

### 1. Install (2 minutes)

```bash
# Clone or download the project
git clone https://github.com/mishrabirupakhya71-code/Cricket-Match-Simulator.git
cd Cricket-Match-Simulator

# Install dependencies
pip install -r requirements.txt
```

### 2. Run (1 minute)

```bash
python desktop_simulator/main.py
```

### 3. Create a Match (2 minutes)

Follow the menu:
1. Select **"1. Create New Match"**
2. Enter match name: `India vs Pakistan`
3. Select total overs: `20`
4. Select team size: `11`
5. Choose batting and bowling teams
6. Start simulation!

---

## 🎮 Your First Match

### Main Menu

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
```

### Step-by-Step: Create a Match

**Step 1: Select Option 1**
```
Choose option: 1
```

**Step 2: Enter Match Details**
```
Match Name: India vs Pakistan
Total Overs: 20
Team Size: 11
```

**Step 3: Select Teams**
```
Select batting team captain: (choose from list)
Select bowling team captain: (choose from list)
```

**Step 4: Start Simulation**
The match begins! You'll see:
```
Over 1.0: Runs: 4 (boundary!)
Over 1.1: Runs: 1
Over 1.2: Runs: 0 (dot ball)
```

### During Match

- **Press 's'** - Simulate next ball
- **Press 'p'** - Pause match
- **Press 'e'** - End innings
- **Press 'q'** - Quit match

---

## 📊 View Results

After the match ends, you'll see:

### Match Summary
```
Match: India vs Pakistan
Batting Team Score: 165/8 (20 overs)
Bowling Team Score: 168/5 (18.3 overs)
Winner: Bowling Team
```

### Batting Statistics
```
Player Name    Runs  Balls  SR     4s  6s
Virat Kohli    45    32     140.6  4   2
MS Dhoni       38    28     135.7  3   1
```

### Bowling Statistics
```
Player Name      Overs  Runs  Wkts  Econ
Jasprit Bumrah   4      28    2     7.0
Yuzvendra Chahal 3.2    22    1     6.6
```

### Fantasy Leaderboard
```
Rank  Player              Fantasy Points
1.    Virat Kohli         95
2.    Jasprit Bumrah      85
3.    MS Dhoni            78
```

---

## 🎯 Next: Try These

### 1. Create Another Match
```
Option: 1
Match Name: Australia vs England
Total Overs: 20
Team Size: 11
```

### 2. Manage Players
```
Option: 3
Add New Player
Enter Player Name: Babar Azam
Enter Average: 50.5
Enter Strike Rate: 135
```

### 3. View Rankings
```
Option: 4
```

View global rankings of all players across all matches!

### 4. Run Tests
```
pytest tests/ -v
```

See all 150+ tests pass!

---

## 🚀 Pro Tips

✅ **Create multiple players** for better variety
✅ **Run tests** to verify everything works
✅ **Try different team sizes** (5v5, 8v8, 11v11)
✅ **Check leaderboards** after each match
✅ **Use Custom SQL** for advanced queries

---

## 📚 Learn More

- **[Installation Guide](Installation-Guide)** - Detailed setup
- **[Using the Simulator](Using-the-Simulator)** - Complete usage guide
- **[Cricket Logic](Cricket-Logic)** - How cricket rules work
- **[Fantasy Points](Fantasy-Points-System)** - Points calculation

---

## 🆘 Troubleshooting

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "Database locked"
Just wait a moment and try again - it auto-unlocks.

### Need more help?
See [FAQ](FAQ) or [Troubleshooting](Troubleshooting)

---

## ✨ You're Ready!

**Your Cricket Match Simulator is now running!** 🏏

Enjoy simulating cricket matches and tracking fantasy points!
