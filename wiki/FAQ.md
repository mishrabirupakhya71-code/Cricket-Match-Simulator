# Frequently Asked Questions (FAQ)

Answers to common questions about the Cricket Match Simulator.

---

## 🚀 Installation & Setup

### Q: What are the system requirements?
**A:** Python 3.10 or higher, 2GB RAM, ~500MB disk space. See [System Requirements](System-Requirements) for details.

### Q: How do I install the project?
**A:** Follow the [Installation Guide](Installation-Guide). Quick version:
```bash
git clone https://github.com/mishrabirupakhya71-code/Cricket-Match-Simulator.git
cd Cricket-Match-Simulator
pip install -r requirements.txt
python desktop_simulator/main.py
```

### Q: Can I run it on Windows/Mac/Linux?
**A:** Yes! All three operating systems are supported. See [Installation Guide](Installation-Guide) for OS-specific instructions.

### Q: I'm getting "ModuleNotFoundError"
**A:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Q: Do I need a virtual environment?
**A:** Recommended but not required. Virtual environments isolate your Python packages. See [Installation Guide](Installation-Guide) for setup.

---

## 🎮 Usage Questions

### Q: How do I create a match?
**A:** From the main menu, select option 1 "Create New Match". See [Using the Simulator](Using-the-Simulator) for detailed steps.

### Q: What team sizes are supported?
**A:** Any size! 5v5, 8v8, 11v11, 7v7, etc. The all-out condition automatically adjusts: (team_size - 1) wickets.

### Q: Can I pause a match?
**A:** Yes! Press 'p' during simulation to pause. Resume later with "Resume Match" option.

### Q: How long does a match take?
**A:** About 2-5 minutes depending on team size and your simulation speed. Each ball takes a few seconds.

### Q: Can I add custom players?
**A:** Yes! Select option 3 "Manage Players" from the main menu.

### Q: How do I view player rankings?
**A:** Select option 4 "Global Rankings" from the main menu.

---

## 📊 Cricket & Fantasy Points

### Q: How are fantasy points calculated?
**A:** See [Fantasy Points System](Fantasy-Points-System) for complete breakdown. Quick version:
- Batting: 1 point per run + bonuses for 4s and 6s
- Bowling: 25 points per wicket + bonuses for maidens and good economy

### Q: What wicket dismissal types are there?
**A:** 6 types: Bowled, Caught, LBW, Run Out, Stumped, Timed Out. See [Cricket Logic](Cricket-Logic) for details.

### Q: How does strike rotation work?
**A:** Odd runs (1,3,5) rotate strike. Even runs (0,2,4,6) don't. End of over always rotates. See [Cricket Logic](Cricket-Logic) for full explanation.

### Q: What's a maiden over?
**A:** An over where no runs are scored off the bat. Worth 12 fantasy points.

### Q: How is all-out determined?
**A:** When (team_size - 1) batsmen are dismissed. Example: 11v11 cricket = all-out at 10 wickets.

---

## 🧪 Testing

### Q: How do I run tests?
**A:** Use pytest:
```bash
pytest tests/ -v
```

### Q: How many tests are there?
**A:** 150+ test cases covering all cricket logic and fantasy points.

### Q: Do all tests pass?
**A:** Yes! GitHub Actions runs tests automatically on every push. You can see results in the "Actions" tab.

### Q: What's code coverage?
**A:** 100% - all code paths are tested. See [Testing Guide](Testing-Guide) for details.

### Q: Can I run specific tests?
**A:** Yes:
```bash
# Specific file
pytest tests/test_cricket_logic.py -v

# Specific test
pytest tests/test_cricket_logic.py::TestStrikeRotation -v
```

---

## 🗄️ Database

### Q: Where is the database stored?
**A:** `cricket_data.db` in the project root directory. Auto-created on first run.

### Q: Can I view the database?
**A:** Yes, use SQLite:
```bash
sqlite3 cricket_data.db
.tables
SELECT * FROM players;
```

### Q: How do I backup the database?
**A:** Simply copy `cricket_data.db`:
```bash
cp cricket_data.db cricket_data_backup.db
```

### Q: Can I use custom SQL?
**A:** Yes! Select option 6 "Custom SQL" from the main menu.

### Q: What tables are in the database?
**A:** 10 tables: players, matches, teams, innings, ball_by_ball, batting_stats, bowling_stats, fantasy_stats, global_rankings, team_members. See [Database Guide](Database-Guide) for details.

---

## 🐛 Troubleshooting

### Q: I get "Database locked" error
**A:** Wait a few seconds and try again. The database auto-unlocks. Only one instance can write at a time.

### Q: The simulator won't start
**A:** 
1. Check Python version: `python --version` (need 3.10+)
2. Install dependencies: `pip install -r requirements.txt`
3. Check for errors in console

### Q: No output appears
**A:** Try running with Python directly:
```bash
python -u desktop_simulator/main.py
```

### Q: Can't import modules
**A:** Install requirements:
```bash
pip install --upgrade -r requirements.txt
```

See [Troubleshooting](Troubleshooting) for more solutions.

---

## 💾 Saving & Loading

### Q: Are matches automatically saved?
**A:** Yes! Matches are saved to the database when created or paused.

### Q: How do I resume a match?
**A:** Select option 2 "Resume Match" from the main menu.

### Q: Can I delete a match?
**A:** Not from the UI, but you can use Custom SQL to delete from database:
```sql
DELETE FROM matches WHERE id = 1;
```

---

## 🚀 Performance

### Q: How many matches can I create?
**A:** Unlimited! Database can handle thousands of matches.

### Q: Will it slow down with many players?
**A:** No, with proper indexing. We have 100+ players tested.

### Q: Can I simulate very long matches?
**A:** Yes! 50-over matches, T20, etc. all work fine.

---

## 📖 Documentation

### Q: Where's the complete documentation?
**A:** See [Home](Home) for all wiki pages.

### Q: Is there an API?
**A:** No external API. It's a desktop application. See [API Reference](API-Reference) for code API.

### Q: How do I contribute?
**A:** See [Contributing](Contributing) guide for details.

---

## 🆘 Getting Help

### Q: Where do I report bugs?
**A:** Open an issue on GitHub: https://github.com/mishrabirupakhya71-code/Cricket-Match-Simulator/issues

### Q: How do I request a feature?
**A:** Use GitHub Issues with "feature request" label or see [Contributing](Contributing).

### Q: Can I fork and modify?
**A:** Yes! Project is MIT licensed. See [LICENSE](../LICENSE).

### Q: Is there a community?
**A:** Star/watch the GitHub repo to stay updated. See [Contributing](Contributing) to join development.

---

## 📚 Related Pages

- [Installation Guide](Installation-Guide)
- [Using the Simulator](Using-the-Simulator)
- [Cricket Logic](Cricket-Logic)
- [Fantasy Points System](Fantasy-Points-System)
- [Troubleshooting](Troubleshooting)
- [Contributing](Contributing)

---

**Didn't find your answer? Open an issue on GitHub!** 🎉
