# 📑 Complete Project Index

## 🎯 Quick Navigation

### 🏏 Get Started (5 minutes)
1. [README.md](README.md) - Overview & features
2. [SETUP.md](SETUP.md) - Installation & deployment
3. `python desktop_simulator/main.py` - Run simulator

### 📚 Documentation
- [README.md](README.md) - Features, usage, quick start
- [SETUP.md](SETUP.md) - Complete setup guide
- [This file](INDEX.md) - Complete project index

---

## 📁 Project Structure

### Root Files
```
├── README.md               👈 START HERE
├── SETUP.md               📖 Setup guide
├── INDEX.md               📑 This file
├── requirements.txt       🔧 Dependencies
└── LICENSE                📄 License
```

### Desktop Simulator Module
```
desktop_simulator/
├── main.py               (500 lines)  Entry point & menu
├── models.py             (150 lines)  Data models
├── database_manager.py   (700 lines)  SQLite operations
├── match_engine.py       (400 lines)  Ball simulation
├── fantasy_engine.py     (300 lines)  Fantasy points
├── ui_console.py         (300 lines)  Console UI
└── match_state_manager.py (100 lines) Pause/resume
```

### Test Suite
```
tests/
├── test_cricket_logic.py   (2000 lines) 50+ tests
├── test_fantasy_points.py  (1500 lines) 40+ tests
├── test_strike_rotation.py (900 lines)  30+ tests
└── test_database.py        (900 lines)  30+ tests
```

---

## 🚀 Installation & Running

### Quick Install
```bash
cd "d:\New project"
pip install -r requirements.txt
```

### Run Desktop Simulator
```bash
python desktop_simulator/main.py
```

### Run Tests
```bash
pytest tests/ -v
```

---

## 📖 Documentation Map

### For Users
- **README.md** - What can this system do?
- **SETUP.md** - How do I install it?
- [Using Desktop Simulator](#desktop-simulator-usage)

### For Developers
- [Architecture](#architecture)
- [Code Files](#code-file-descriptions)

### For Deployment
- **SETUP.md** - Production deployment section

---

## 🎮 Desktop Simulator Usage

### Main Menu
```
1. Create New Match
2. Resume Match
3. Manage Players
4. Global Rankings
5. Recent Matches
6. Custom SQL
7. Exit
```

### Creating a Match
1. Select "Create New Match"
2. Enter match name
3. Select total overs (usually 20)
4. Select team size (5v5, 8v8, 11v11, etc.)
5. Choose batting team
6. Choose bowling team
7. Start simulation

### Simulating Balls
- Press 's' to simulate next ball
- View live scorecard
- Press 'p' to pause
- Press 'e' to end innings
- View fantasy points at end

### View Results
- Batting statistics
- Bowling statistics
- Match leaderboard
- Special awards
- Global rankings

---

## 🧪 Testing

### Run Tests
```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=desktop_simulator --cov-report=html

# Specific test file
pytest tests/test_cricket_logic.py -v

# Specific test
pytest tests/test_cricket_logic.py::TestStrikeRotation::test_odd_run_rotation -v
```

### Test Categories
- **Cricket Logic** (50 tests) - Strike rotation, all-out, wickets, extras
- **Fantasy Points** (40 tests) - Points, bonuses, awards, leaderboards
- **Strike Rotation** (30 tests) - All rotation scenarios
- **Database** (30 tests) - CRUD operations, persistence

### Expected Results
- ✅ All 150+ tests pass
- ✅ 100% code coverage
- ✅ 0 failures or warnings

---

## 🗄️ Database

### SQLite Database
- **File**: `cricket_data.db` (auto-created)
- **Tables**: 10 normalized tables
- **Location**: `d:\New project\`

### Main Tables
1. **players** - Player information
2. **matches** - Match details
3. **teams** - Team configuration
4. **innings** - Innings tracking
5. **ball_by_ball** - Every ball data
6. **batting_stats** - Batting statistics
7. **bowling_stats** - Bowling statistics
8. **fantasy_stats** - Fantasy points
9. **global_rankings** - Leaderboards
10. **team_members** - Team rosters

### Access Database
```bash
# View database
sqlite3 cricket_data.db

# Common queries
.tables
.schema players
SELECT * FROM players;
SELECT * FROM matches;
SELECT * FROM fantasy_stats;
```

---

## 🏗️ Architecture

### Layers

**UI Layer**
- Desktop: Console (colorama, prettytable)

**Business Logic Layer**
- MatchEngine - Simulate balls
- FantasyEngine - Calculate points
- MatchStateManager - Pause/resume

**Data Access Layer**
- DatabaseManager - SQLite operations

**Storage Layer**
- SQLite3 (desktop)

### Design Patterns
- MVC - Desktop simulator
- Repository - Database access
- Singleton - Database connections

---

## 💾 Code File Descriptions

### desktop_simulator/main.py
**Purpose**: Application entry point and menu system
**Key Classes**: `CricketSimulator`
**Key Methods**:
- `main_menu()` - Menu navigation
- `create_new_match()` - Match setup
- `run_match()` - Main simulation loop
- `manage_players()` - Player management

### desktop_simulator/models.py
**Purpose**: Data model definitions
**Key Classes**: `Player`, `Match`, `Innings`, `Ball`, `BattingStats`, `BowlingStats`, `FantasyStats`
**Key Features**: Type hints, dataclass decorators

### desktop_simulator/database_manager.py
**Purpose**: SQLite database operations
**Key Classes**: `DatabaseManager`
**Key Methods**:
- `add_player()` - Insert player
- `create_match()` - Create match record
- `add_ball()` - Record ball
- `get_statistics()` - Query stats

### desktop_simulator/match_engine.py
**Purpose**: Cricket simulation logic
**Key Classes**: `MatchEngine`
**Key Methods**:
- `simulate_ball()` - Generate one ball
- `check_wicket()` - Determine if out
- `calculate_runs()` - Compute runs
- `rotate_strike()` - Update batsman

### desktop_simulator/fantasy_engine.py
**Purpose**: Fantasy points calculation
**Key Classes**: `FantasyEngine`
**Key Methods**:
- `calculate_batting_points()` - Batter fantasy points
- `calculate_bowling_points()` - Bowler fantasy points
- `get_leaderboard()` - Fantasy ranking
- `award_special_awards()` - Special achievements

### desktop_simulator/match_state_manager.py
**Purpose**: Match pause/resume functionality
**Key Classes**: `MatchStateManager`
**Key Methods**:
- `save_state()` - Save match state
- `load_state()` - Restore match state
- `pause_match()` - Pause simulation
- `resume_match()` - Continue simulation

### desktop_simulator/ui_console.py
**Purpose**: Console UI components
**Key Classes**: `UIConsole`
**Key Methods**:
- `display_scorecard()` - Show match score
- `display_menu()` - Show menu
- `get_user_input()` - Input handling
- `format_stats_table()` - Format statistics

---

## 🧪 Test Files

### test_cricket_logic.py
Tests for cricket simulation logic:
- Strike rotation (odd/even runs)
- Wicket types (all 6 types)
- Extras handling (wides, no-balls, etc)
- All-out conditions
- Over progression

### test_fantasy_points.py
Tests for fantasy points:
- Batting points calculation
- Bowling points calculation
- Leaderboard functionality
- Special awards
- Edge cases and boundaries

### test_strike_rotation.py
Comprehensive strike rotation tests:
- Single runs (1, 3, 5)
- Pairs (2, 4, 6)
- Boundaries
- Wickets
- End of over

### test_database.py
Database operation tests:
- Player CRUD operations
- Match creation
- Ball recording
- Statistics retrieval
- Database integrity

---

## 📦 Dependencies

### Core
- `sqlite3` - Database (built-in)
- `python-dateutil` - Date handling
- `pytz` - Timezone support

### UI
- `colorama` - Terminal colors
- `prettytable` - Table formatting

### Testing
- `pytest` - Test framework
- `pytest-cov` - Code coverage

---

## 🚀 Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Run tests: `pytest tests/ -v`
3. ✅ Start simulator: `python desktop_simulator/main.py`
4. ✅ Create matches and simulate cricket
5. ✅ View statistics and leaderboards

**Your cricket simulator is ready! 🏏**
