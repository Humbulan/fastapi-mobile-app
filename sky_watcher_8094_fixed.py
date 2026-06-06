#!/usr/bin/env python3
"""
Sky Watcher - Port 8094
Military Airspace Monitoring (Fixed Version)
"""

from flask import Flask, jsonify
import time
import random
import threading
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='[%(asctime)s] %(message)s',
                   datefmt='%Y-%m-%d %H:%M:%S')

# Airspace data
aircraft_detections = []
lock = threading.Lock()

def simulate_radar():
    """Simulate radar scanning"""
    global aircraft_detections
    while True:
        time.sleep(30)  # Scan every 30 seconds
        with lock:
            # Random aircraft detection
            if random.random() < 0.3:  # 30% chance of detection
                aircraft = {
                    "callsign": f"AE{random.randint(1000, 9999)}",
                    "type": random.choice(["Military Transport", "Fighter Jet", "Reconnaissance"]),
                    "altitude": random.randint(25000, 40000),
                    "timestamp": time.time()
                }
                aircraft_detections.append(aircraft)
                logging.info(f"🛩️ DETECTED: {aircraft['type']} - {aircraft['callsign']}")
            
            # Keep last 20 detections
            aircraft_detections = aircraft_detections[-20:]

@app.route('/')
def home():
    return jsonify({
        "service": "Sky Watcher - Intel Redirect",
        "port": 8094,
        "status": "online",
        "timestamp": time.time()
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "port": 8094,
        "uptime": "active"
    })

@app.route('/api/airspace')
def airspace():
    with lock:
        return jsonify({
            "zone": "Limpopo Airspace",
            "bounds": {"min_lat": -25.0, "max_lat": -22.0, "min_lon": 29.0, "max_lon": 32.0},
            "active_alerts": len([a for a in aircraft_detections if a.get('type') == 'Fighter Jet']),
            "recent_detections": aircraft_detections[-5:],
            "timestamp": time.time()
        })

if __name__ == '__main__':
    logging.info("🚀 Sky Watcher starting on port 8094...")
    # Start radar simulation in background
    threading.Thread(target=simulate_radar, daemon=True).start()
    # Run Flask
    app.run(host='0.0.0.0', port=8094, debug=False, threaded=True)
