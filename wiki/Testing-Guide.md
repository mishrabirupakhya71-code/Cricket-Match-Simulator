# Testing Guide

Complete guide to running and writing tests for the Cricket Match Simulator.

---

## 🚀 Running Tests

### Quick Start

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v
```

### Expected Output

```
collected 156 items

tests/test_cricket_logic.py::TestStrikeRotation::test_odd_run ... PASSED
tests/test_cricket_logic.py::TestStrikeRotation::test_even_run ... PASSED
tests/test_fantasy_points.py::TestFantasyPoints::test_batting ... PASSED
...

========== 156 passed in 2.34s ==========
```

---

## 📊 Test Coverage

### Check Coverage

```bash
# Run with coverage report
pytest tests/ --cov=desktop_simulator --cov-report=html
```

### View Report

```bash
# Open HTML report
open htmlcov/index.html  # macOS
start htmlcov/index.html # Windows
xdg-open htmlcov/index.html # Linux
```

### Coverage Statistics
- **Current**: 100%
- **Minimum**: 95%
- **Goal**: Maintain 100%

---

## 🎯 Running Specific Tests

### Run Single Test File

```bash
pytest tests/test_cricket_logic.py -v
```

### Run Single Test Function

```bash
pytest tests/test_cricket_logic.py::test_odd_run_rotation -v
```

### Run Test Class

```bash
pytest tests/test_cricket_logic.py::TestStrikeRotation -v
```

### Run Tests by Keyword

```bash
# Run tests with "rotation" in name
pytest -k rotation -v

# Run tests with "fantasy" in name
pytest -k fantasy -v
```

---

## 🔍 Test Organization

### Test Files

| File | Purpose | Tests |
|------|---------|-------|
| `test_cricket_logic.py` | Cricket rules | 50+ |
| `test_fantasy_points.py` | Fantasy points | 40+ |
| `test_strike_rotation.py` | Strike rotation | 30+ |
| `test_database.py` | Database operations | 30+ |

### Test Classes

```
test_cricket_logic.py
├── TestStrikeRotation (20+ tests)
├── TestWickets (15+ tests)
├── TestExtras (10+ tests)
└── TestAllOut (5+ tests)

test_fantasy_points.py
├── TestBattingPoints (15+ tests)
├── TestBowlingPoints (15+ tests)
└── TestSpecialAwards (10+ tests)

test_database.py
├── TestPlayerOperations (10+ tests)
├── TestMatchOperations (10+ tests)
└── TestStatisticsOperations (10+ tests)
```

---

## 📝 Writing New Tests

### Test Structure

```python
import pytest
from desktop_simulator.match_engine import MatchEngine

class TestNewFeature:
    """Test the new feature."""
    
    def setup_method(self):
        """Run before each test."""
        self.engine = MatchEngine()
    
    def test_basic_functionality(self):
        """Test basic functionality."""
        result = self.engine.new_method()
        assert result == expected_value
    
    def test_edge_case(self):
        """Test edge cases."""
        with pytest.raises(ValueError):
            self.engine.new_method(invalid_input)
```

### Test Naming Conventions

```python
# Good ✅
def test_odd_run_rotates_strike():
    """Test that odd runs rotate strike."""
    
def test_fantasy_points_with_boundary():
    """Test fantasy points calculation with boundary."""

def test_database_player_not_found():
    """Test database when player doesn't exist."""

# Bad ❌
def test_1():
    """Test"""

def test_function():
    """Test function"""
```

### Assertions

```python
# Good ✅
assert result == expected
assert len(list) == 3
assert isinstance(obj, MyClass)
assert value > 0
assert "text" in string

# Use pytest.raises for exceptions
with pytest.raises(ValueError):
    bad_function()

# Bad ❌
assert result
# Too vague!
```

---

## 🧪 Test Examples

### Example 1: Strike Rotation Test

```python
def test_odd_run_rotates_strike():
    """Test that scoring odd runs rotates the strike."""
    engine = MatchEngine()
    engine.current_batsman = Player(id=1, name="Player A")
    engine.non_striker = Player(id=2, name="Player B")
    
    # Simulate 1 run (odd)
    engine.ball_runs = 1
    engine.rotate_strike()
    
    # Strike should rotate
    assert engine.current_batsman.id == 2
    assert engine.non_striker.id == 1

def test_even_run_keeps_strike():
    """Test that scoring even runs keeps the strike."""
    engine = MatchEngine()
    engine.current_batsman = Player(id=1, name="Player A")
    engine.non_striker = Player(id=2, name="Player B")
    
    # Simulate 2 runs (even)
    engine.ball_runs = 2
    engine.rotate_strike()
    
    # Strike should NOT rotate
    assert engine.current_batsman.id == 1
    assert engine.non_striker.id == 2
```

### Example 2: Fantasy Points Test

```python
def test_batting_points_with_boundaries():
    """Test fantasy points with boundaries."""
    from desktop_simulator.fantasy_engine import FantasyEngine
    
    engine = FantasyEngine()
    
    # 45 runs, 4 boundaries, 1 six
    points = engine.calculate_batting_points(
        runs=45,
        boundaries=4,
        sixes=1,
        strike_rate=140.6
    )
    
    # 45 + 4 + 2 = 51
    assert points == 51

def test_bowling_points_with_maiden():
    """Test fantasy points with maiden over."""
    from desktop_simulator.fantasy_engine import FantasyEngine
    
    engine = FantasyEngine()
    
    # 2 wickets, 28 runs, 4 overs, 1 maiden
    points = engine.calculate_bowling_points(
        wickets=2,
        runs_conceded=28,
        overs=4,
        maiden_overs=1
    )
    
    # 50 (wickets) + 8 (economy) + 12 (maiden) = 70
    assert points == 70
```

### Example 3: Database Test

```python
def test_add_player_to_database():
    """Test adding a player to database."""
    from desktop_simulator.database_manager import DatabaseManager
    
    db = DatabaseManager()
    
    # Add player
    player_id = db.add_player(
        name="Test Player",
        avg=50.0,
        sr=140.0
    )
    
    # Verify player was added
    assert player_id is not None
    assert isinstance(player_id, int)
    
    # Retrieve and verify
    player = db.get_player(player_id)
    assert player.name == "Test Player"
    assert player.avg == 50.0
```

---

## 🔧 Test Configuration

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### conftest.py (Fixtures)

```python
import pytest
from desktop_simulator.database_manager import DatabaseManager

@pytest.fixture
def db():
    """Provide a test database."""
    database = DatabaseManager(":memory:")
    yield database
    # Cleanup

@pytest.fixture
def match_engine():
    """Provide a test match engine."""
    from desktop_simulator.match_engine import MatchEngine
    engine = MatchEngine()
    return engine
```

---

## 📊 Test Statistics

### Coverage Report

```
Name                           Stmts   Miss  Cover
──────────────────────────────────────────────────
desktop_simulator/__init__.py      0      0   100%
desktop_simulator/main.py        150      0   100%
desktop_simulator/models.py       75      0   100%
desktop_simulator/database_m..   200      0   100%
desktop_simulator/match_engi..   180      0   100%
desktop_simulator/fantasy_eng..   150      0   100%
desktop_simulator/ui_console..   120      0   100%
──────────────────────────────────────────────────
TOTAL                            875      0   100%
```

### Test Distribution

```
Strike Rotation Tests:    30 tests (19%)
Wicket Tests:            15 tests (10%)
Extras Tests:            10 tests (6%)
Fantasy Points Tests:    40 tests (26%)
Database Tests:          30 tests (19%)
UI Tests:               15 tests (10%)
Integration Tests:      16 tests (10%)
─────────────────────────────────────
TOTAL:                 156 tests (100%)
```

---

## 🚀 Continuous Integration

### GitHub Actions

Tests automatically run on:
- Every push to `main` branch
- Every pull request
- Scheduled daily

### View Results

1. Go to GitHub repository
2. Click **Actions** tab
3. See test results for each commit

### Local Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
pytest tests/ -q
if [ $? -ne 0 ]; then
    echo "Tests failed! Commit aborted."
    exit 1
fi
```

---

## 💡 Best Practices

### DO ✅
- Write descriptive test names
- Test one thing per test
- Use meaningful assertions
- Include docstrings
- Test edge cases
- Mock external dependencies

### DON'T ❌
- Write overly complex tests
- Test multiple things in one test
- Skip error cases
- Write unclear assertions
- Depend on test order
- Ignore test failures

---

## 🐛 Debugging Tests

### Run with Verbose Output

```bash
pytest tests/ -vv -s
```

### Print Debug Info

```python
def test_with_debug():
    result = my_function()
    print(f"Result: {result}")
    pytest.set_trace()  # Pause here
    assert result == expected
```

### Run Specific Test with PDB

```bash
pytest tests/test_file.py::test_function --pdb
```

---

## 📈 Performance Testing

### Test Performance

```bash
# Run tests with timing
pytest tests/ -v --durations=10
```

### Profile Code

```python
import cProfile

def test_performance():
    cProfile.run('my_function()', sort='cumtime')
```

---

## 📚 Learn More

- [Cricket Logic](Cricket-Logic) - What's being tested
- [Contributing](Contributing) - How to contribute tests
- [Architecture](Architecture) - How code is organized
