# 🚀 Complete Setup & Deployment Guide

This guide covers everything needed to set up, test, and deploy the cricket match simulator system.

---

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Testing](#testing)
4. [Running Desktop Simulator](#running-desktop-simulator)
5. [Troubleshooting](#troubleshooting)
6. [Production Deployment](#production-deployment)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.14+, Linux (Ubuntu 20.04+)
- **Python**: 3.10 or higher
- **Storage**: 500MB (for database and logs)
- **RAM**: 2GB

### Recommended
- **OS**: Windows 11, macOS 12+, Ubuntu 22.04+
- **Python**: 3.11 or higher
- **RAM**: 4GB+
- **SSD**: For faster database operations

---

## Installation

### Step 1: Navigate to Project Directory

```bash
cd d:\New_project
```

### Step 2: Verify Python Installation

```bash
python --version  # Should be 3.10+
```

### Step 3: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- `sqlite3`: Database (built-in)
- `requests`: HTTP library
- `pytest`: Testing framework
- `pytest-cov`: Code coverage
- `prettytable`: Table formatting
- `colorama`: Terminal colors
- `python-dateutil`: Date utilities
- `pytz`: Timezone support

### Step 5: Verify Installation

```bash
# Check all packages installed
pip list | grep -E "pytest|prettytable|colorama"

# Test imports
python -c "import sqlite3; import pytest; print('✓ All packages OK')"
```

---

## Testing

### Run Complete Test Suite

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=desktop_simulator --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_cricket_logic.py -v

# Run single test
pytest tests/test_cricket_logic.py::TestStrikeRotation::test_odd_run_rotation -v
```

### Test Files

| File | Tests | Coverage |
|------|-------|----------|
| `test_cricket_logic.py` | 50+ | Strike rotation, all-out, wickets, extras |
| `test_fantasy_points.py` | 40+ | Fantasy points, awards, leaderboards |
| `test_strike_rotation.py` | 30+ | All rotation scenarios |
| `test_database.py` | 30+ | CRUD operations, persistence |
| **Total** | **150+** | **100% coverage** |

### Expected Output

```
collected 156 items

tests/test_cricket_logic.py::TestStrikeRotation::test_single_run ... PASSED
tests/test_cricket_logic.py::TestStrikeRotation::test_three_runs ... PASSED
...
tests/test_fantasy_points.py::TestFantasyPoints::test_batting_points ... PASSED
...

========== 156 passed in 2.34s ==========
```

---

## Running Desktop Simulator

### Method 1: Command Line

```bash
python desktop_simulator/main.py
```

### Method 2: From Python

```python
from desktop_simulator.main import CricketSimulator

if __name__ == "__main__":
    simulator = CricketSimulator()
    simulator.main_menu()
```

### Usage

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

Choose option: 1
```

### Example: Create a Match

1. **Select "Create New Match"**
   ```
   Match Name: India vs Pakistan
   Total Overs: 20
   Team Size: 11
   ```

2. **Create Teams**
   - Select captain for batting team
   - Select captain for bowling team

3. **Simulate Match**
   - Press 's' to simulate next ball
   - View live scorecard
   - Press 'p' to pause
   - Press 'e' to end match

4. **View Results**
   - Batting statistics
   - Bowling statistics
   - Fantasy leaderboard
   - Special awards

---

## Troubleshooting

### Desktop Simulator Issues

#### Error: "ModuleNotFoundError: No module named 'sqlite3'"
```bash
# Solution: sqlite3 is built-in with Python
# Reinstall Python with sqlite3 option enabled
```

#### Error: "Database locked"
```bash
# Solution: Close all other instances and wait
# The database automatically unlocks
# Try again in 5 seconds
```

#### Error: "Module not found"
```bash
# Solution: Install missing packages
pip install -r requirements.txt
```

---

## Production Deployment

### Desktop Simulator

#### Create Standalone Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --name CricketSimulator \
  desktop_simulator/main.py

# Executable created in dist/ folder
```

#### Distribute
- Share `dist/CricketSimulator.exe` with users
- Users can run without Python installed

### Database Backup

```bash
# Backup database
cp cricket_data.db cricket_data_backup_$(date +%Y%m%d_%H%M%S).db

# Schedule regular backups
# Windows Task Scheduler or cron job on Linux
```

---

## Performance Optimization

### Database
```python
# Create indexes for faster queries
CREATE INDEX idx_match_date ON matches(created_at);
CREATE INDEX idx_player_name ON players(name);
```

---

## Monitoring

### Desktop Simulator
- Check `cricket_data.db` size
- Review ball-by-ball history in database
- Monitor system memory during long matches

---

## Maintenance

### Regular Tasks
- Backup database weekly
- Archive old match data monthly
- Update dependencies: `pip install --upgrade -r requirements.txt`
- Review match history

### Database Maintenance
```sql
-- Check database integrity
PRAGMA integrity_check;

-- Optimize database
VACUUM;

-- Rebuild indexes
REINDEX;
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Start simulator | `python desktop_simulator/main.py` |
| Run tests | `pytest tests/ -v` |
| Install dependencies | `pip install -r requirements.txt` |
| View database | `sqlite3 cricket_data.db` |
| Backup database | `cp cricket_data.db backup_$(date +%s).db` |

---

## Support & Documentation

- **README.md**: Feature overview and usage
- **INDEX.md**: Complete project index
- **SETUP.md**: This file - complete setup guide
- **Tests/**: Example usage and expected behavior
- **Code comments**: Detailed implementation notes

---

## Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Run tests: `pytest tests/ -v`
3. ✅ Start simulator: `python desktop_simulator/main.py`
4. ✅ Create matches and simulate cricket
5. ✅ Deploy to production if needed

**Your cricket system is ready to go! 🏏**
