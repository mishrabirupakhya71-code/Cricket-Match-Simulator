# Troubleshooting Guide

Solutions to common issues with the Cricket Match Simulator.

---

## 🚀 Installation Issues

### "Python not found"

**Error:**
```
'python' is not recognized as an internal or external command
```

**Solutions:**

1. **Check Python Installation**
```bash
python --version
```

If not recognized, Python isn't installed or not in PATH.

2. **Try Python3**
```bash
python3 --version
python3 desktop_simulator/main.py
```

3. **Add Python to PATH (Windows)**
- Go to Control Panel → Environment Variables
- Edit PATH to include Python installation directory
- Restart terminal

### "pip not found"

**Error:**
```
'pip' is not recognized
```

**Solutions:**

1. **Use Python module**
```bash
python -m pip --version
python -m pip install -r requirements.txt
```

2. **Upgrade pip**
```bash
python -m pip install --upgrade pip
```

### "Module not found"

**Error:**
```
ModuleNotFoundError: No module named 'pytest'
```

**Solutions:**

```bash
# Reinstall all dependencies
pip install --upgrade -r requirements.txt

# Or install specific package
pip install pytest pytest-cov colorama prettytable
```

---

## 🎮 Runtime Issues

### Database Locked

**Error:**
```
sqlite3.OperationalError: database is locked
```

**Causes:**
- Another instance is using the database
- Previous instance didn't close properly

**Solutions:**

1. **Wait a moment**
```bash
# Wait 5-10 seconds and try again
```

2. **Close other instances**
- Make sure only one simulator is running

3. **Delete lock file** (if exists)
```bash
rm cricket_data.db-wal
rm cricket_data.db-shm
```

4. **Restart the application**

### No Output Displayed

**Error:**
- Nothing appears when running simulator
- Program seems frozen

**Solutions:**

1. **Run with unbuffered output**
```bash
python -u desktop_simulator/main.py
```

2. **Check for errors**
```bash
python desktop_simulator/main.py 2>&1 | cat
```

3. **Run from PowerShell** (Windows)
```powershell
python desktop_simulator/main.py
```

### Memory Usage High

**Error:**
- Simulator uses lots of memory
- Computer becomes slow

**Solutions:**

1. **Close other applications**
2. **Use smaller team sizes** (try 5v5 instead of 11v11)
3. **Don't run many matches simultaneously**

---

## 🧪 Testing Issues

### Tests Won't Run

**Error:**
```
pytest: command not found
```

**Solution:**
```bash
pip install pytest pytest-cov
pytest tests/ -v
```

### Some Tests Fail

**Error:**
```
FAILED tests/test_cricket_logic.py::test_function
```

**Solutions:**

1. **Check Python version**
```bash
python --version  # Need 3.10+
```

2. **Reinstall dependencies**
```bash
pip install --upgrade -r requirements.txt
```

3. **Check database**
```bash
rm cricket_data.db  # Delete and recreate
```

4. **Run specific test**
```bash
pytest tests/test_cricket_logic.py -v -s
```

### Tests Run Slowly

**Error:**
- Tests take too long

**Solutions:**

1. **Run in parallel**
```bash
pip install pytest-xdist
pytest tests/ -n auto
```

2. **Skip slow tests**
```bash
pytest tests/ -m "not slow"
```

---

## 🗄️ Database Issues

### Database Corrupted

**Symptoms:**
- Strange data
- Mismatched records
- Errors when querying

**Solution:**

1. **Backup current database**
```bash
cp cricket_data.db cricket_data_backup.db
```

2. **Delete and recreate**
```bash
rm cricket_data.db
# Run simulator - new DB will be created
python desktop_simulator/main.py
```

### Can't Access Database

**Error:**
```
sqlite3.OperationalError: unable to open database file
```

**Solutions:**

1. **Check file permissions**
```bash
ls -l cricket_data.db  # Check permissions
chmod 644 cricket_data.db  # Fix permissions
```

2. **Check disk space**
```bash
df -h  # Check available space
```

3. **Verify file exists**
```bash
ls -la cricket_data.db
```

---

## 🎯 Feature Issues

### Match Won't Simulate

**Symptoms:**
- Stuck at simulation screen
- No balls are simulated

**Solutions:**

1. **Check if match is properly created**
2. **Verify players are added**
3. **Try smaller team size**

### Rankings Not Updating

**Symptoms:**
- Rankings show old data
- New matches don't affect rankings

**Solutions:**

```bash
# Force update rankings
python -c "
from desktop_simulator.database_manager import DatabaseManager
db = DatabaseManager()
db.calculate_global_rankings()
"
```

### Fantasy Points Incorrect

**Symptoms:**
- Points don't match expectations
- Calculations seem wrong

**Solutions:**

1. **Verify cricket logic**
2. **Check Fantasy Points guide**
3. **Report as bug with details**

---

## 🔧 System-Specific Issues

### Windows Issues

#### Terminal Shows Garbage Characters

**Solution:**
```powershell
# Use -NoExit flag
python desktop_simulator/main.py -NoExit

# Or use UTF-8 encoding
chcp 65001
python desktop_simulator/main.py
```

#### Permission Denied

**Solution:**
```powershell
# Run as Administrator
# Or use --user flag
pip install --user -r requirements.txt
```

### macOS Issues

#### Permission Denied

**Solution:**
```bash
chmod +x desktop_simulator/main.py
python desktop_simulator/main.py
```

#### M1/M2 Compatibility

**Solution:**
```bash
# Use native Python for ARM
python3 --version
python3 desktop_simulator/main.py
```

### Linux Issues

#### Cannot Write to Directory

**Solution:**
```bash
# Check ownership
ls -la

# Change ownership
sudo chown $USER: .

# Or run with sudo
sudo python desktop_simulator/main.py
```

---

## 🐛 Reporting Issues

### What to Include

When reporting a bug, include:

1. **Error message** - Exact error text
2. **Steps to reproduce** - How to trigger the bug
3. **System info** - OS, Python version, etc.
4. **Log output** - Full console output

### How to Report

1. **Search existing issues** - May already be fixed
2. **Click "New Issue"** on GitHub
3. **Choose "Bug report" template**
4. **Fill in details**
5. **Click "Submit"**

### Example Bug Report

```
Title: Database locked error on startup

Description:
Whenever I try to start the simulator, I get a database locked error.

Steps to Reproduce:
1. Run python desktop_simulator/main.py
2. Select option 1 to create match
3. Error appears

System Info:
- OS: Windows 11
- Python: 3.11.2
- Error: sqlite3.OperationalError: database is locked

Expected:
Match creation should work

Actual:
Database lock error occurs
```

---

## ✅ Diagnostics

### Run Diagnostics

```python
# Create a test script
import sqlite3
import pytest
from desktop_simulator.database_manager import DatabaseManager

print("✓ Checking system...")
print(f"✓ Python version: {import sys; sys.version}")

try:
    db = DatabaseManager()
    print("✓ Database connection: OK")
except Exception as e:
    print(f"✗ Database error: {e}")

try:
    import pytest
    print("✓ Pytest installed: OK")
except:
    print("✗ Pytest not installed")

print("✓ Diagnostics complete")
```

---

## 📞 Getting Help

1. **Check FAQ** - Common questions answered
2. **Search issues** - Problem might be known
3. **Read documentation** - Solution usually documented
4. **Open issue** - Describe the problem
5. **Provide logs** - Include error messages

---

## 🆘 Emergency Help

### Nuclear Option: Start Fresh

```bash
# Remove everything
rm -rf cricket_data.db
rm -rf venv/
rm -rf .pytest_cache/
rm -rf __pycache__/

# Reinstall
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run
python desktop_simulator/main.py
```

---

## 📚 Learn More

- [FAQ](FAQ) - Frequently asked questions
- [Installation Guide](Installation-Guide) - Setup help
- [Using the Simulator](Using-the-Simulator) - How to use

**Still stuck? Open an issue on GitHub!** 🎉
