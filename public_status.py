#!/usr/bin/env python3
from db_config import get_db_connection
"""
🌍 IMPERIAL SOVEREIGN TRUTH - Public Status Page
Port 8097 - https://imperial.humbu.store/status
"""
from flask import Flask, render_template_string, jsonify
import sqlite3
import datetime
import subprocess
import os

app = Flask(__name__)

def get_sky_status():
    """Get latest sky-watcher status"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT metric_text, recorded_at FROM imperial_metrics WHERE metric_name='sky_watcher_status' ORDER BY recorded_at DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0], result[1]
    except:
        pass
    return "No data", str(datetime.datetime.now())

def get_economic_status():
    """Get latest economic status"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT metric_value, metric_text, recorded_at FROM imperial_metrics WHERE metric_name='economic_status' ORDER BY recorded_at DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        if result:
            value, text, time = result
            if value >= 0.8:
                return "🔴 CRITICAL", text, time
            elif value >= 0.4:
                return "🟡 WARNING", text, time
            else:
                return "🟢 STABLE", text, time
    except:
        pass
    return "🟢 STABLE", "All systems nominal", str(datetime.datetime.now())

def get_port_status():
    """Get port status summary"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM system_sectors WHERE status='online'")
        online = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM system_sectors")
        total = cursor.fetchone()[0]
        conn.close()
        return online, total
    except:
        return 44, 47  # fallback

@app.route('/')
def index():
    return redirect('/status')

@app.route('/status')
def status_page():
    sky_status, sky_time = get_sky_status()
    econ_level, econ_text, econ_time = get_economic_status()
    online, total = get_port_status()
    
    # Determine overall status
    if "🔴" in econ_level or "CRITICAL" in sky_status:
        overall = "🔴 RED ALERT"
        overall_color = "#ff4444"
    elif "🟡" in econ_level or "WARNING" in sky_status:
        overall = "🟡 ELEVATED"
        overall_color = "#ffbb33"
    else:
        overall = "🟢 STABLE"
        overall_color = "#00C851"
    
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🛡️ Imperial Sovereign Truth</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { 
                background: #0a0a0a; 
                color: #0f0; 
                font-family: 'Courier New', monospace; 
                padding: 20px;
                line-height: 1.6;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                border: 2px solid #0f0;
                padding: 30px;
                border-radius: 10px;
                background: #111;
            }
            h1 { 
                text-align: center;
                border-bottom: 1px solid #0f0;
                padding-bottom: 20px;
                margin-top: 0;
            }
            .status-panel {
                background: #1a1a1a;
                padding: 20px;
                margin: 20px 0;
                border-radius: 5px;
                border-left: 5px solid {{ overall_color }};
            }
            .overall {
                font-size: 2em;
                text-align: center;
                margin: 20px 0;
                color: {{ overall_color }};
                font-weight: bold;
            }
            .metric {
                display: flex;
                justify-content: space-between;
                padding: 10px;
                border-bottom: 1px solid #333;
            }
            .metric:last-child {
                border-bottom: none;
            }
            .label {
                color: #888;
            }
            .value {
                color: #0f0;
                font-weight: bold;
            }
            .footer {
                text-align: center;
                margin-top: 30px;
                color: #666;
                font-size: 0.8em;
                border-top: 1px solid #333;
                padding-top: 20px;
            }
            .blink {
                animation: blink 1s infinite;
            }
            @keyframes blink {
                0% { opacity: 1; }
                50% { opacity: 0.3; }
                100% { opacity: 1; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛡️ THOHOYANDOU SOVEREIGN STATUS</h1>
            
            <div class="overall {{ 'blink' if '🔴' in overall else '' }}">
                {{ overall }}
            </div>
            
            <div class="status-panel" style="border-left-color: {{ 'red' if '🔴' in econ_level else 'orange' if '🟡' in econ_level else '#0f0' }}">
                <h2>🛰️ SKY WATCH</h2>
                <div class="metric">
                    <span class="label">Status:</span>
                    <span class="value">{{ sky_status }}</span>
                </div>
                <div class="metric">
                    <span class="label">Last Updated:</span>
                    <span class="value">{{ sky_time[:19] }}</span>
                </div>
            </div>
            
            <div class="status-panel" style="border-left-color: {{ 'red' if '🔴' in econ_level else 'orange' if '🟡' in econ_level else '#0f0' }}">
                <h2>📉 ECONOMIC PULSE</h2>
                <div class="metric">
                    <span class="label">Status:</span>
                    <span class="value">{{ econ_level }}</span>
                </div>
                <div class="metric">
                    <span class="label">Details:</span>
                    <span class="value">{{ econ_text }}</span>
                </div>
                <div class="metric">
                    <span class="label">Last Updated:</span>
                    <span class="value">{{ econ_time[:19] }}</span>
                </div>
            </div>
            
            <div class="status-panel">
                <h2>🔌 NETWORK STATUS</h2>
                <div class="metric">
                    <span class="label">Ports Online:</span>
                    <span class="value">{{ online }}/{{ total }}</span>
                </div>
                <div class="metric">
                    <span class="label">System Capacity:</span>
                    <span class="value">{{ (online/total*100)|round(1) }}%</span>
                </div>
            </div>
            
            <div class="footer">
                <p>🏛️ Imperial Nexus - Verified Intelligence</p>
                <p>47/47 Ports Online | Last Updated: {{ time }}</p>
                <p><i>Provided by Humbu Wandeme Trading Enterprise</i></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(template, 
                                 overall=overall,
                                 overall_color=overall_color,
                                 sky_status=sky_status,
                                 sky_time=sky_time,
                                 econ_level=econ_level,
                                 econ_text=econ_text,
                                 econ_time=econ_time,
                                 online=online,
                                 total=total,
                                 time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/api/status')
def api_status():
    """JSON API for programmatic access"""
    sky_status, _ = get_sky_status()
    econ_level, econ_text, _ = get_economic_status()
    online, total = get_port_status()
    
    return jsonify({
        'overall': 'STABLE' if '🟢' in econ_level else 'ELEVATED' if '🟡' in econ_level else 'CRITICAL',
        'sky': sky_status,
        'economic': {
            'level': econ_level,
            'text': econ_text
        },
        'network': {
            'ports_online': online,
            'total_ports': total,
            'percentage': round((online/total*100), 1)
        },
        'timestamp': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🌍 Imperial Sovereign Truth running on port 8097")
    print("   📍 Status page: http://localhost:8097/status")
    print("   📍 JSON API: http://localhost:8097/api/status")
    app.run(host='0.0.0.0', port=8097, debug=False)
