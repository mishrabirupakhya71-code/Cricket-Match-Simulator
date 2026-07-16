# Installation Guide

This guide will help you install and set up the Cricket Match Simulator on your system.

## 📋 Prerequisites

Before you start, make sure you have:
- **Python 3.10+** installed
- **pip** (Python package manager)
- **SQLite3** (included with Python)
- ~500MB free disk space
- 2GB RAM minimum

### Check Python Version

```bash
python --version  # Should be 3.10 or higher
```

---

## 🪟 Windows Installation

### Step 1: Download the Project

**Option A: Using Git**
```bash
git clone https://github.com/mishrabirupakhya71-code/Cricket-Match-Simulator.git
cd Cricket-Match-Simulator
```

**Option B: Download ZIP**
1. Visit https://github.com/mishrabirupakhya71-code/Cricket-Match-Simulator
2. Click **Code** → **Download ZIP**
3. Extract the ZIP file
4. Open Command Prompt or PowerShell
5. Navigate to the project folder

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

You should see `(venv)` at the start of your terminal line.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python -c "import sqlite3; import pytest; print('✓ Installation successful!')"
```

### Step 5: Run the Simulator

```bash
python desktop_simulator/main.py
```

---

## 🍎 macOS Installation

### Step 1: Download the Project

```bash
git clone https://github.com/mishrabirupakhya71-code/Cricket-Match-Simulator.git
cd Cricket-Match-Simulator
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python -c "import sqlite3; import pytest; print('✓ Installation successful!')"
```

### Step 5: Run the Simulator

```bash
python desktop_simulator/main.py
```

---

## 🐧 Linux Installation (Ubuntu/Debian)

### Step 1: Install Python (if needed)

```bash
sudo apt-get update
sudo apt-get install python3.10 python3-pip python3-venv
```

### Step 2: Download the Project

```bash
git clone https://github.com/mishrabirupakhya71-code/Cricket-Match-Simulator.git
cd Cricket-Match-Simulator
```

### Step 3: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Verify Installation

```bash
python -c "import sqlite3; import pytest; print('✓ Installation successful!')"
```

### Step 6: Run the Simulator

```bash
python desktop_simulator/main.py
```

---

## 📦 Dependencies

The project requires these Python packages:

| Package | Purpose |
|---------|---------|
| `sqlite3` | Database (built-in) |
| `pytest` | Testing framework |
| `pytest-cov` | Coverage reporting |
| `prettytable` | Table formatting |
| `colorama` | Terminal colors |
| `python-dateutil` | Date utilities |
| `pytz` | Timezone support |

All are listed in `requirements.txt` and installed with one command.

---

## ✅ Verification Steps

After installation, verify everything works:

### 1. Check Python Packages

```bash
pip list | grep pytest
pip list | grep colorama
```

### 2. Run Tests

```bash
pytest tests/ -v
```

You should see:
```
collected 156 items
... 156 passed in X.XXs
```

### 3. Start the Simulator

```bash
python desktop_simulator/main.py
```

You should see the menu:
```
┌─────────────────────────────────────┐
│   🏏 CRICKET MATCH SIMULATOR 🏏     │
├─────────────────────────────────────┤
│  1. Create New Match                │
│  ...
```

---

## 🔧 Troubleshooting Installation

### Error: "Python not found"
```bash
# Make sure Python is installed
python --version

# Or use python3
python3 --version
```

### Error: "pip not found"
```bash
# Upgrade pip
python -m pip install --upgrade pip
```

### Error: "Module not found"
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Error: "Permission denied" (Linux/macOS)
```bash
# Use --user flag
pip install --user -r requirements.txt
```

---

## 🎯 Next Steps

After successful installation:

1. **[Quick Start](Quick-Start)** - Get running in 5 minutes
2. **[Using the Simulator](Using-the-Simulator)** - Learn how to use it
3. **[Running Tests](Testing-Guide)** - Run the test suite

---

## 💡 Tips

- Always activate the virtual environment before running the simulator
- Keep `requirements.txt` updated if you install new packages
- Use `pip list` to see all installed packages
- Check Python version compatibility (3.10+)

---

## 🆘 Need Help?

- See [FAQ](FAQ) for common questions
- Check [Troubleshooting](Troubleshooting) for solutions
- Open an issue on GitHub for problems
