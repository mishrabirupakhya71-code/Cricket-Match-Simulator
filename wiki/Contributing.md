# Contributing

Thank you for your interest in contributing to the Cricket Match Simulator! Here's how you can help.

---

## 📋 Getting Started

### Step 1: Fork the Repository
1. Go to https://github.com/mishrabirupakhya71-code/Cricket-Match-Simulator
2. Click **Fork** (top right)
3. This creates your own copy

### Step 2: Clone Your Fork
```bash
git clone https://github.com/YOUR_USERNAME/Cricket-Match-Simulator.git
cd Cricket-Match-Simulator
```

### Step 3: Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### Step 4: Install Development Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Make Your Changes
Edit files and create features.

### Step 6: Run Tests
```bash
pytest tests/ -v
```

Ensure all tests pass!

### Step 7: Commit Your Changes
```bash
git add .
git commit -m "Add: feature description"
```

### Step 8: Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### Step 9: Create a Pull Request
1. Go to your fork on GitHub
2. Click **Compare & pull request**
3. Describe your changes
4. Click **Create pull request**

---

## 🎯 Types of Contributions

### 🐛 Bug Fixes
- Fix errors in existing code
- Fix cricket logic issues
- Fix fantasy points calculation

**Steps:**
1. Create issue describing the bug
2. Fork and fix on a branch
3. Submit PR with fixes
4. Reference issue in PR

### ✨ New Features
- Add new cricket rule
- Add new statistics
- Improve UI/UX
- Add new commands

**Steps:**
1. Discuss in an issue first
2. Wait for approval
3. Implement feature with tests
4. Submit PR

### 📖 Documentation
- Fix typos in README
- Improve wiki pages
- Add code comments
- Create tutorials

**Steps:**
1. Edit documentation files
2. Submit PR directly
3. No tests needed for docs

### 🧪 Tests
- Add test cases
- Increase coverage
- Test edge cases
- Test cricket logic

**Steps:**
1. Write test in appropriate file
2. Ensure test passes
3. Submit PR

---

## 📝 Code Guidelines

### Style

Follow **PEP 8** Python style guide:
```python
# Good ✅
def calculate_fantasy_points(runs, wickets):
    """Calculate fantasy points for a player."""
    batting_points = runs * 1
    bowling_points = wickets * 25
    return batting_points + bowling_points

# Bad ❌
def cfp(r,w):
    return r*1 + w*25
```

### Naming

- **Functions**: `lowercase_with_underscores()`
- **Classes**: `PascalCase`
- **Constants**: `UPPERCASE_WITH_UNDERSCORES`
- **Variables**: `lowercase_with_underscores`

### Comments

```python
# Good ✅
# Calculate fantasy points with bonuses
def calculate_points(runs, boundaries):
    """
    Calculate fantasy points for batsman.
    
    Args:
        runs: Total runs scored
        boundaries: Number of 4s and 6s
        
    Returns:
        int: Total fantasy points
    """
    pass

# Bad ❌
# add points
def ap(r, b):
    pass
```

### Type Hints

```python
# Good ✅
def calculate_points(runs: int, wickets: int) -> int:
    return runs + wickets * 25

# Bad ❌
def calculate_points(runs, wickets):
    pass
```

---

## 🧪 Testing Requirements

### Write Tests for New Features

```python
# In appropriate test file
def test_new_feature():
    """Test the new feature works correctly."""
    result = new_feature(input_data)
    assert result == expected_output

def test_new_feature_edge_case():
    """Test edge cases."""
    result = new_feature(edge_case_input)
    assert result == edge_case_output
```

### Run Tests Before Submitting

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=desktop_simulator

# Run specific test
pytest tests/test_file.py::test_function -v
```

### Coverage Requirements
- **Minimum**: 95% code coverage
- **Goal**: 100% coverage
- Use: `pytest --cov`

---

## 📋 Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code follows PEP 8 style guide
- [ ] All tests pass: `pytest tests/ -v`
- [ ] Code coverage ≥ 95%
- [ ] Added docstrings to new functions
- [ ] Added type hints
- [ ] Updated relevant documentation
- [ ] Commits have clear messages
- [ ] No merge conflicts

### PR Title Format

```
[TYPE] Brief description

Types:
- [FEATURE] Add new functionality
- [FIX] Fix a bug
- [DOCS] Documentation update
- [TEST] Test additions
- [REFACTOR] Code refactoring
- [PERF] Performance improvement
```

### PR Description Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issue
Fixes #123

## Testing
- Tested on Windows/Mac/Linux
- All tests pass
- Added new tests

## Screenshots (if applicable)
```

---

## 🔄 Code Review Process

1. **Automated Checks**: GitHub Actions runs tests
2. **Manual Review**: Maintainer reviews code
3. **Feedback**: Changes may be requested
4. **Approval**: PR approved once issues resolved
5. **Merge**: Your changes are merged!

---

## 🚀 Development Workflow

### Setting Up Dev Environment

```bash
# Clone fork
git clone https://github.com/YOUR_USERNAME/Cricket-Match-Simulator.git
cd Cricket-Match-Simulator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install dev tools (optional)
pip install black flake8 mypy
```

### Making Changes

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes
# Edit files...

# Run tests
pytest tests/ -v

# Format code (optional)
black desktop_simulator/

# Commit
git commit -m "Add: my new feature"

# Push
git push origin feature/my-feature
```

### Updating Fork

```bash
# Add upstream remote
git remote add upstream https://github.com/mishrabirupakhya71-code/Cricket-Match-Simulator.git

# Fetch latest
git fetch upstream

# Rebase your branch
git rebase upstream/main
```

---

## 🎯 Areas for Contribution

### High Priority
- 🐛 Bug fixes
- 📖 Documentation improvements
- 🧪 Additional test cases
- ♻️ Code refactoring

### Nice to Have
- ✨ UI improvements
- 📊 New statistics
- 🎯 Performance optimization
- 🌍 Internationalization

---

## 📞 Getting Help

- **Questions?** Open an issue or discussion
- **Unclear?** Ask in comments
- **Stuck?** Reach out on GitHub
- **Chat?** Start a discussion

---

## ✅ Recognition

Contributors will be:
- ✅ Added to CONTRIBUTORS file
- ✅ Mentioned in release notes
- ✅ Recognized in README

---

## 📄 License

By contributing, you agree that your contributions are licensed under the MIT License.

---

## 🎉 Thank You!

Your contributions make this project better! Every PR, issue, and comment helps.

**Happy coding!** 🏏

---

## 📚 Learn More

- [Code Structure](Code-Structure) - Project organization
- [Testing Guide](Testing-Guide) - How to write tests
- [Architecture](Architecture) - System design
