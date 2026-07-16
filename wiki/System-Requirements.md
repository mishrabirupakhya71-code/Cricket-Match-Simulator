# System Requirements

Complete system requirements for running the Cricket Match Simulator.

---

## 📋 Minimum Requirements

### Hardware
- **CPU**: Any modern processor (Intel/AMD)
- **RAM**: 2GB minimum
- **Disk Space**: 500MB free space
- **Display**: 80x24 terminal (basic text mode)

### Software
- **Operating System**: 
  - Windows 10 or higher
  - macOS 10.14 or higher
  - Linux (Ubuntu 20.04, Debian 11, etc.)
- **Python**: 3.10, 3.11, or 3.12
- **pip**: Python package manager
- **SQLite3**: Built-in with Python

---

## 🚀 Recommended Specifications

### Hardware
- **CPU**: Intel i5/i7 or equivalent
- **RAM**: 4GB or more
- **Disk Space**: SSD with 1GB+ free space
- **Display**: Full HD (1920x1080) terminal for better UI

### Software
- **Python**: 3.11 or 3.12 (latest stable)
- **Terminal**: Modern terminal emulator with UTF-8 support
- **Git**: For cloning repository

---

## 🪟 Windows Requirements

### Versions
- Windows 10 (build 19041 or later)
- Windows 11 (all versions)

### Software to Install
1. **Python** - Download from python.org
2. **pip** - Included with Python
3. **Git** (optional) - For cloning repository

### Installation
```bash
# Download Python installer
# Run installer (check "Add Python to PATH")
# Verify
python --version
pip --version

# Clone repository
git clone https://github.com/mishrabirupakhya71-code/Cricket-Match-Simulator.git

# Install dependencies
pip install -r requirements.txt
```

### Terminal Recommendation
- PowerShell (Windows 11 recommended)
- Windows Terminal (Modern, recommended)
- Command Prompt (Basic, works fine)

### Troubleshooting
- If "python not found": Add Python to PATH
- If "pip not found": Use `python -m pip`
- If colors don't show: Use Windows Terminal instead of CMD

---

## 🍎 macOS Requirements

### Versions
- macOS 10.14 or higher
- macOS 11 (Big Sur) or later recommended

### Software to Install
1. **Python** - From python.org or Homebrew
2. **Xcode Command Line Tools**
3. **Git** (optional) - For cloning

### Installation
```bash
# Install Xcode tools (if needed)
xcode-select --install

# Install Python (if needed)
brew install python

# Verify
python3 --version
pip3 --version

# Clone repository
git clone https://github.com/mishrabirupakhya71-code/Cricket-Match-Simulator.git

# Install dependencies
pip3 install -r requirements.txt
```

### M1/M2 Mac Specific
- Use `python3` instead of `python`
- Should work natively (no Rosetta needed)
- Ensure ARM64 Python version installed

### Terminal Recommendation
- Terminal.app (built-in, works fine)
- iTerm2 (Advanced, optional)

---

## 🐧 Linux Requirements

### Distributions
- Ubuntu 20.04 LTS or higher
- Debian 11 or higher
- Fedora 34+
- Arch Linux
- Other modern distributions

### Software to Install
1. **Python 3.10+** - From package manager
2. **pip** - Python package manager
3. **Git** - For cloning

### Installation (Ubuntu/Debian)
```bash
# Update packages
sudo apt update

# Install Python and dependencies
sudo apt install -y python3.10 python3-pip python3-venv

# Verify
python3 --version
pip3 --version

# Clone repository
git clone https://github.com/mishrabirupakhya71-code/Cricket-Match-Simulator.git
cd Cricket-Match-Simulator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Installation (Fedora)
```bash
# Install Python
sudo dnf install python3.10 python3-pip

# Clone and setup (same as above)
```

### Terminal Recommendation
- GNOME Terminal (Ubuntu default, works great)
- Konsole (KDE)
- Any modern terminal with UTF-8 support

---

## 📦 Python Version Support

### Supported Versions
| Version | Support | Status |
|---------|---------|--------|
| **3.12** | ✅ Full | Latest, tested |
| **3.11** | ✅ Full | Stable, recommended |
| **3.10** | ✅ Full | Older, still works |
| **3.9** | ❌ Not | Too old |
| **2.7** | ❌ Not | Obsolete |

### Check Your Version
```bash
python --version  # or python3 --version
```

### Update Python
```bash
# Windows
# Download from python.org and reinstall

# macOS
brew upgrade python

# Ubuntu/Debian
sudo apt update && sudo apt install -y python3
```

---

## 📚 Dependencies

### Core Dependencies
| Package | Purpose | Size |
|---------|---------|------|
| `sqlite3` | Database (built-in) | ~5MB |
| `pytest` | Testing | ~1MB |
| `pytest-cov` | Coverage | ~500KB |
| `colorama` | Colors | ~100KB |
| `prettytable` | Tables | ~100KB |
| `python-dateutil` | Dates | ~500KB |
| `pytz` | Timezones | ~2MB |

### Total Dependencies
- **Total Size**: ~15-20MB after installation
- **Installation Time**: ~1-2 minutes (depends on internet)

### Install All
```bash
pip install -r requirements.txt
```

---

## 🧪 Testing Requirements

### For Running Tests
```bash
pip install pytest pytest-cov
```

### Test Environment
- Can run on minimal hardware
- Uses ~100-200MB RAM during test execution
- Tests complete in <5 seconds

### Run Tests
```bash
pytest tests/ -v
```

---

## 📊 Performance

### Expected Performance

| Operation | Time | Hardware |
|-----------|------|----------|
| Start app | <1s | Any |
| Create match | 1-2s | Any |
| Simulate 20 overs | 2-5 min | Any |
| Run all tests | <5s | Moderate |
| Database operations | <100ms | Any |

### Optimization Tips
- Use SSD for faster database operations
- Close other applications for better performance
- Use Python 3.11+ for best performance

---

## 🔌 Network Requirements

### No Internet Required
- Application works completely offline
- No cloud connectivity needed
- No external API calls

### Optional Network
- GitHub for downloading code
- Package repository for installing dependencies (one-time)

---

## ♿ Accessibility

### Terminal Requirements
- UTF-8 encoding support (for emojis and symbols)
- 80+ columns width (standard terminal size)
- Mouse support (optional, keyboard works fine)

### Enabling UTF-8
```bash
# Windows (PowerShell)
chcp 65001

# Linux/macOS (usually automatic)
echo $LANG
```

---

## 🔐 Security

### Safe to Run
- No root/admin privileges needed
- No network connections by default
- No data collection or telemetry
- Local database only
- MIT License (open source)

### Security Notes
- Run from trusted source only
- Don't disable antivirus
- Keep Python updated
- Use virtual environment (recommended)

---

## 📱 Supported Platforms

### Tested On
- ✅ Windows 10/11
- ✅ macOS 11+
- ✅ Ubuntu 20.04+
- ✅ Debian 11+
- ✅ Fedora 34+
- ✅ Alpine Linux
- ✅ Docker (containerized)

### Not Tested
- iOS
- Android
- Raspberry Pi (should work, not tested)
- Older systems (<2010)

---

## 🚀 Getting Started

### Quick Check

```bash
# Verify requirements
python --version         # Should be 3.10+
pip --version           # Should be present
python -c "import sqlite3; print('✓ SQLite OK')"

# Install project
git clone https://github.com/mishrabirupakhya71-code/Cricket-Match-Simulator.git
cd Cricket-Match-Simulator
pip install -r requirements.txt

# Run
python desktop_simulator/main.py
```

---

## 📚 Learn More

- [Installation Guide](Installation-Guide) - Complete setup
- [Quick Start](Quick-Start) - Get running in 5 minutes
- [Troubleshooting](Troubleshooting) - Fix issues
