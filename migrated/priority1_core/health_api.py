from db_config import get_db_connection
from flask import Flask, jsonify
import sqlite3
import os
import psutil
from datetime import datetime

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'database': check_database(),
            'memory': psutil.virtual_memory().percent,
            'cpu': psutil.cpu_percent(),
            'uptime': get_uptime()
        }
    })

@app.route('/metrics')
def metrics():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get today's transactions
    cursor.execute("SELECT COUNT(*), SUM(amount) FROM transactions WHERE date(timestamp) = date('now')")
    today = cursor.fetchone()
    
    # Get village activity
    cursor.execute("SELECT COUNT(DISTINCT village) FROM marketplace WHERE timestamp > datetime('now', '-1 day')")
    active_villages = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'today_transactions': today[0] or 0,
        'today_revenue': today[1] or 0,
        'active_villages': active_villages,
        'total_villages': 40,
        'system_load': os.getloadavg()[0]
    })

def check_database():
    try:
        conn = get_db_connection()
        conn.execute("SELECT 1")
        conn.close()
        return 'connected'
    except:
        return 'disconnected'

def get_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            return str(int(uptime_seconds / 3600)) + 'h'
    except:
        return 'unknown'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=False)
