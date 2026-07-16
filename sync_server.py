"""
Sync Server for Cricket Data Collector
Receives data synced from phone and integrates with desktop database
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import base64
import sqlite3
from datetime import datetime
from pathlib import Path


app = Flask(__name__)
CORS(app)

# Configuration
SYNC_DB_PATH = 'cricket_data.db'
SYNC_LOG_FILE = 'sync_log.txt'
UPLOADS_DIR = Path('synced_data')
UPLOADS_DIR.mkdir(exist_ok=True)


def init_sync_db():
    """Initialize sync database."""
    conn = sqlite3.connect(SYNC_DB_PATH)
    cursor = conn.cursor()
    
    # Create sync records table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sync_records (
            sync_id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            sync_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_count INTEGER,
            status TEXT,
            file_path TEXT
        )
    ''')
    
    conn.commit()
    return conn


def log_sync(message: str):
    """Log sync event."""
    with open(SYNC_LOG_FILE, 'a') as f:
        f.write(f"[{datetime.now().isoformat()}] {message}\n")


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'version': '1.0',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/sync', methods=['POST'])
def sync_data():
    """Receive synced cricket data from phone."""
    try:
        device_id = request.headers.get('X-Device-ID', 'unknown')
        
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Validate data
        if 'version' not in data or data['version'] != 1:
            return jsonify({
                'success': False,
                'message': 'Invalid data version'
            }), 400
        
        # Save raw data
        filename = f"sync_{device_id}_{datetime.now().timestamp()}.json"
        filepath = UPLOADS_DIR / filename
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Process synced balls
        unsynced_balls = data.get('unsyncedBalls', [])
        matches = data.get('matches', [])
        
        # Store in database
        conn = init_sync_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sync_records (device_id, data_count, status, file_path)
            VALUES (?, ?, ?, ?)
        ''', (device_id, len(unsynced_balls), 'completed', str(filepath)))
        
        conn.commit()
        conn.close()
        
        # Log
        log_sync(f"Received sync from {device_id}: {len(unsynced_balls)} balls, {len(matches)} matches")
        
        return jsonify({
            'success': True,
            'message': f'Received {len(unsynced_balls)} balls',
            'device_id': device_id,
            'sync_id': cursor.lastrowid,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        log_sync(f"Sync error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Sync failed: {str(e)}'
        }), 500


@app.route('/sync/import', methods=['POST'])
def import_sync_code():
    """Import data from sync code."""
    try:
        data = request.get_json()
        sync_code = data.get('sync_code', '')
        
        if not sync_code:
            return jsonify({
                'success': False,
                'message': 'No sync code provided'
            }), 400
        
        # Decompress sync code
        try:
            json_str = base64.b64decode(sync_code).decode('utf-8')
            decoded_data = json.loads(json_str)
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Invalid sync code: {str(e)}'
            }), 400
        
        # Validate
        if decoded_data.get('version') != 1:
            return jsonify({
                'success': False,
                'message': 'Invalid data version'
            }), 400
        
        # Save
        device_id = decoded_data.get('deviceId', 'unknown')
        filename = f"imported_{device_id}_{datetime.now().timestamp()}.json"
        filepath = UPLOADS_DIR / filename
        
        with open(filepath, 'w') as f:
            json.dump(decoded_data, f, indent=2)
        
        # Log
        log_sync(f"Imported sync code from {device_id}: {len(decoded_data.get('unsyncedBalls', []))} balls")
        
        return jsonify({
            'success': True,
            'message': 'Data imported successfully',
            'balls_count': len(decoded_data.get('unsyncedBalls', [])),
            'file_path': str(filepath)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Import failed: {str(e)}'
        }), 500


@app.route('/sync/list', methods=['GET'])
def list_syncs():
    """List all sync records."""
    try:
        conn = init_sync_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT sync_id, device_id, sync_timestamp, data_count, status
            FROM sync_records
            ORDER BY sync_timestamp DESC
            LIMIT 50
        ''')
        
        records = []
        for row in cursor.fetchall():
            records.append({
                'sync_id': row[0],
                'device_id': row[1],
                'timestamp': row[2],
                'data_count': row[3],
                'status': row[4]
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'records': records
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to list syncs: {str(e)}'
        }), 500


@app.route('/sync/export', methods=['GET'])
def export_sync_data():
    """Export synced data as JSON."""
    try:
        # Combine all synced data
        all_data = {
            'version': 1,
            'export_timestamp': datetime.now().isoformat(),
            'syncs': []
        }
        
        # Read all synced files
        for filepath in UPLOADS_DIR.glob('sync_*.json'):
            with open(filepath, 'r') as f:
                data = json.load(f)
                all_data['syncs'].append({
                    'file': filepath.name,
                    'data': data
                })
        
        return jsonify(all_data)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Export failed: {str(e)}'
        }), 500


@app.route('/sync/stats', methods=['GET'])
def sync_stats():
    """Get sync statistics."""
    try:
        conn = init_sync_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*), SUM(data_count) FROM sync_records WHERE status = ?', ('completed',))
        result = cursor.fetchone()
        
        total_syncs = result[0] or 0
        total_balls = result[1] or 0
        
        # Count unique devices
        cursor.execute('SELECT COUNT(DISTINCT device_id) FROM sync_records')
        unique_devices = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return jsonify({
            'success': True,
            'total_syncs': total_syncs,
            'total_balls_synced': total_balls,
            'unique_devices': unique_devices,
            'synced_files': len(list(UPLOADS_DIR.glob('sync_*.json'))),
            'imported_files': len(list(UPLOADS_DIR.glob('imported_*.json')))
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get stats: {str(e)}'
        }), 500


@app.route('/sync/retrieve', methods=['POST'])
def retrieve_sync_file():
    """Retrieve a specific synced file."""
    try:
        data = request.get_json()
        file_id = data.get('file_id', '')
        
        filepath = UPLOADS_DIR / f"sync_{file_id}.json"
        
        if not filepath.exists():
            return jsonify({
                'success': False,
                'message': 'File not found'
            }), 404
        
        with open(filepath, 'r') as f:
            file_data = json.load(f)
        
        return jsonify({
            'success': True,
            'data': file_data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to retrieve: {str(e)}'
        }), 500


if __name__ == '__main__':
    # Initialize database
    init_sync_db()
    
    # Log startup
    log_sync("Sync Server started")
    
    # Run server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )
