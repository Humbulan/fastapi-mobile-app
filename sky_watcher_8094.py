#!/usr/bin/env python3
from db_config import get_db_connection
"""
🛰️ SKY-WATCHER - Military Airspace Monitoring
Port 8094 (Intel Redirect)
Monitors Limpopo airspace for military aircraft
"""
import requests
import json
import time
import sqlite3
from datetime import datetime
import os

# Limpopo/Border monitoring zone
WATCH_ZONE = {
    "min_lat": -25.0, "max_lat": -22.0, 
    "min_lon": 29.0, "max_lon": 32.0
}

# Military transponder hex codes (simplified - in production would query database)
MILITARY_HEX = ['AE01', 'AE02', 'AE03', 'AE04', 'AE05']  # Example codes

class SkyWatcher:
    def __init__(self):
        self.log_file = "logs/sky_watcher.log"
        os.makedirs("logs", exist_ok=True)
        self.alerts = []
        
    def scan_airspace(self):
        """Scan for military aircraft in Limpopo airspace"""
        # In production, this would hit ADSB-Exchange or OpenSky API
        # Simulated for now - in real implementation, replace with actual API call
        military_detected = 0
        aircraft_list = []
        
        # Simulate detection based on time of day (for demo)
        current_hour = datetime.now().hour
        if 6 <= current_hour <= 18:  # Daytime operations
            if current_hour % 3 == 0:  # Every 3 hours, simulate a military flight
                military_detected = 1
                aircraft_list.append({
                    'hex': 'AE01' + str(current_hour),
                    'type': 'Military Transport',
                    'altitude': 28000,
                    'speed': 420,
                    'position': 'Near Hoedspruit'
                })
        
        return military_detected, aircraft_list
    
    def check_threshold(self, military_count):
        """Check if threshold exceeded (3 military aircraft in 1 hour)"""
        # Add to rolling log
        self.alerts.append({
            'timestamp': datetime.now(),
            'count': military_count
        })
        
        # Keep last hour
        one_hour_ago = datetime.now().timestamp() - 3600
        self.alerts = [a for a in self.alerts if a['timestamp'].timestamp() > one_hour_ago]
        
        total_last_hour = sum(a['count'] for a in self.alerts)
        
        if total_last_hour >= 3:
            return True, total_last_hour
        return False, total_last_hour
    
    def log_status(self, status, message):
        """Log to file and console"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {status}: {message}"
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry + '\n')
        
        print(log_entry)
        
        # Update database
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO imperial_metrics (metric_name, metric_value, metric_text, recorded_at)
                VALUES (?, ?, ?, ?)
            ''', ('sky_watcher_status', 1 if 'ALERT' in status else 0, message, datetime.now().isoformat()))
            conn.commit()
            conn.close()
        except:
            pass
    
    def run(self):
        """Main monitoring loop"""
        self.log_status("🟢 INIT", "Sky-Watcher active on Port 8094")
        self.log_status("🛰️ ZONE", f"Monitoring Limpopo airspace: {WATCH_ZONE}")
        
        while True:
            try:
                military_count, aircraft = self.scan_airspace()
                threshold_exceeded, total = self.check_threshold(military_count)
                
                if threshold_exceeded:
                    alert_msg = f"🚨 ALERT: {total} military aircraft detected in last hour"
                    self.log_status("🔴 CRITICAL", alert_msg)
                    
                    # Send SMS alert via USSD gateway
                    try:
                        import requests
                        requests.post('http://localhost:8087/api/send_sms', 
                                     json={'phone': '0794658481', 'message': alert_msg},
                                     timeout=2)
                    except:
                        pass
                elif military_count > 0:
                    self.log_status("🟡 WARNING", f"{military_count} military aircraft detected")
                else:
                    self.log_status("🟢 STABLE", "No military activity detected")
                
                # Log aircraft details if any
                for a in aircraft:
                    self.log_status("🛩️ TRACK", f"{a['type']} - {a['hex']} @ {a['altitude']}ft")
                
                time.sleep(300)  # Check every 5 minutes
                
            except KeyboardInterrupt:
                self.log_status("🛑 TERM", "Sky-Watcher shutting down")
                break
            except Exception as e:
                self.log_status("❌ ERROR", str(e))
                time.sleep(60)

if __name__ == "__main__":
    watcher = SkyWatcher()
    watcher.run()
