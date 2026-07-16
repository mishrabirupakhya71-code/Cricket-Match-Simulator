# 🚀 Complete Setup & Deployment Guide

This guide covers everything needed to set up, test, and deploy the cricket match simulator system.

---

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Testing](#testing)
4. [Running Desktop Simulator](#running-desktop-simulator)
5. [Running Phone App](#running-phone-app)
6. [Running Sync Server](#running-sync-server)
7. [Troubleshooting](#troubleshooting)
8. [Production Deployment](#production-deployment)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.14+, Linux (Ubuntu 20.04+)
- **Python**: 3.10 or higher
- **Browser**: Chrome 90+, Firefox 88+, Edge 90+, Safari 14+
- **Storage**: 500MB (for database and logs)
- **RAM**: 2GB (desktop) + 512MB (phone)

### Recommended
- **OS**: Windows 11, macOS 12+, Ubuntu 22.04+
- **Python**: 3.11 or higher
- **RAM**: 4GB+
- **SSD**: For faster database operations
- **Internet**: For sync server deployment

---

## Installation

### Step 1: Navigate to Project Directory

```bash
cd d:\New project
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
- `flask`: Web framework for sync server
- `flask-cors`: CORS support
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
pip list | grep -E "flask|pytest|prettytable|colorama"

# Test imports
python -c "import sqlite3; import flask; import pytest; print('✓ All packages OK')"
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

## Running Phone App

### Method 1: Local Web Server

```bash
cd phone_app
python -m http.server 8000
```

Then open: `http://localhost:8000`

### Method 2: Direct File Access

```bash
# Windows
start phone_app/index.html

# macOS
open phone_app/index.html

# Linux
xdg-open phone_app/index.html
```

### Method 3: Deploy to Real Server

```bash
# Copy entire phone_app folder to web server
# Ensure HTTPS is enabled (required for PWA)
# Access via: https://your-domain.com/phone_app
```

### Usage on Phone

1. **Open in mobile browser**
   - Visit `http://your-laptop-ip:8000` (on same network)
   - Or scan QR code if deployed

2. **Install as PWA**
   - Android: Menu → "Install app"
   - iOS: Share → "Add to Home Screen"

3. **Create Match**
   - Tap "Matches" tab
   - Tap "+ New Match"
   - Enter match details

4. **Record Balls**
   - Tap "Data Entry" tab
   - Select match
   - Tap "+ Record Ball"
   - Choose runs & wickets

5. **Sync Data**
   - Tap "Sync" tab
   - Copy sync code
   - Send to laptop

---

## Running Sync Server

### Installation

```bash
# Install Flask (if not already installed)
pip install flask flask-cors

# Verify installation
python -c "import flask; print(f'Flask {flask.__version__}')"
```

### Start Server

```bash
python sync_server.py
```

**Expected Output:**
```
 * Running on http://0.0.0.0:5000
 * WARNING: This is a development server. Do not use in production.
 * Use a production WSGI server instead.
```

### Configure Phone App

1. Open phone app
2. Go to "Settings" tab
3. Enter sync URL: `http://your-laptop-ip:5000`
4. Enable "Auto Sync"

### Test Sync Endpoint

```bash
# Health check
curl http://localhost:5000/health

# Get stats
curl http://localhost:5000/sync/stats

# List syncs
curl http://localhost:5000/sync/list
```

### API Reference

#### POST /sync
Receive data from phone

**Request:**
```json
{
  "version": 1,
  "timestamp": "2024-01-15T10:30:00",
  "deviceId": "cricket-abc123",
  "unsyncedBalls": [
    {"over": 1, "ball": 1, "runs": 4}
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Received 5 balls",
  "device_id": "cricket-abc123"
}
```

#### GET /sync/stats
Get synchronization statistics

**Response:**
```json
{
  "success": true,
  "total_syncs": 15,
  "total_balls_synced": 245,
  "unique_devices": 3,
  "synced_files": 15
}
```

---

## Troubleshooting

### Desktop Simulator Issues

#### Error: "ModuleNotFoundError: No module named 'flask'"
```bash
# Solution: Install missing packages
pip install -r requirements.txt
```

#### Error: "Database locked"
```bash
# Solution: Close all other instances and wait
# The database automatically unlocks
# Try again in 5 seconds
```

#### Error: "Port 5000 already in use"
```bash
# Find process using port
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Phone App Issues

#### PWA won't install
- Ensure browser supports PWA (Chrome, Edge, Firefox)
- Check if running on HTTPS (except localhost)
- Clear browser cache
- Try incognito/private mode

#### Data not persisting
- Check storage quota: `localStorage.getItem('storageInfo')`
- Clear cache: Settings tab → "Clear Data"
- Check browser storage limits

#### Sync not working
- Verify network connection
- Check server URL in settings
- Confirm sync server is running
- Check browser console for errors

### Sync Server Issues

#### Can't connect from phone
```bash
# Find your laptop IP
ipconfig  # Windows
ifconfig  # macOS/Linux

# Use that IP from phone: http://192.168.1.100:5000
```

#### CORS errors
```
# Solution: Ensure flask-cors is installed
pip install flask-cors

# Verify in sync_server.py: CORS(app)
```

#### Sync data not appearing
- Check `synced_data/` folder exists
- Check file permissions
- Review `sync_log.txt` for errors

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

### Phone App

#### Deploy to Hosting Service

**Option 1: GitHub Pages**
```bash
git init
git add phone_app/
git commit -m "Cricket app"
git push origin gh-pages

# Access: username.github.io/cricket-app
```

**Option 2: Netlify**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod --dir=phone_app
```

**Option 3: Firebase**
```bash
npm install -g firebase-tools
firebase login
firebase deploy

# Configure firebase.json for phone_app directory
```

### Sync Server

#### Deploy with Gunicorn (Production)

```bash
# Install Gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn -w 4 -b 0.0.0.0:5000 sync_server:app

# Run in background (Linux)
nohup gunicorn -w 4 -b 0.0.0.0:5000 sync_server:app > sync_server.log 2>&1 &
```

#### Deploy with Docker

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY sync_server.py .

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "sync_server:app"]
```

**Build and Run:**
```bash
docker build -t cricket-sync .
docker run -p 5000:5000 cricket-sync
```

#### Enable HTTPS

**Using Let's Encrypt:**
```bash
# Install Certbot
pip install certbot

# Get certificate
certbot certonly --standalone -d yourdomain.com

# Update sync_server.py to use certificate
```

### Database Backup

```bash
# Backup database
cp cricket_data.db cricket_data_backup_$(date +%Y%m%d_%H%M%S).db

# Backup phone sync data
tar -czf synced_data_backup_$(date +%Y%m%d_%H%M%S).tar.gz synced_data/
```

---

## Performance Optimization

### Database
```python
# Create indexes for faster queries
CREATE INDEX idx_match_date ON matches(created_at);
CREATE INDEX idx_player_name ON players(name);
```

### Phone App
- Uses IndexedDB for optimal local storage
- Service Worker caches all assets
- Lazy loading for large match lists

### Sync Server
```bash
# Use production WSGI server
gunicorn -w 4 --worker-class sync_server:app

# Enable gzip compression
# Enable Redis caching for high volume
```

---

## Monitoring

### Desktop Simulator
- Check `cricket_data.db` size
- Review ball-by-ball history in database
- Monitor system memory during long matches

### Phone App
- Storage usage: Settings tab shows percentage
- Check browser console for errors
- Monitor IndexedDB size

### Sync Server
- Check `sync_log.txt` for all operations
- Review `synced_data/` folder size
- Monitor sync statistics: `GET /sync/stats`

---

## Maintenance

### Regular Tasks
- Backup database weekly
- Archive old sync data monthly
- Update dependencies: `pip install --upgrade -r requirements.txt`
- Review and cleanup sync logs

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
| Start sync server | `python sync_server.py` |
| Run tests | `pytest tests/ -v` |
| Install dependencies | `pip install -r requirements.txt` |
| Start phone app server | `cd phone_app && python -m http.server 8000` |
| View database | `sqlite3 cricket_data.db` |
| Backup database | `cp cricket_data.db backup_$(date +%s).db` |

---

## Support & Documentation

- **README.md**: Feature overview and usage
- **SETUP.md**: This file - complete setup guide
- **Tests/**: Example usage and expected behavior
- **Code comments**: Detailed implementation notes

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Run tests to verify installation
3. ✅ Start desktop simulator
4. ✅ Test phone app locally
5. ✅ Configure sync server
6. ✅ Deploy to production

**Your cricket system is ready to go! 🏏**
