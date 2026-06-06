#!/usr/bin/env python3
"""
Imperial Omega Milestone Alert System
Tracks progress to R500B and sends email alerts for key milestones
"""

import json
import smtplib
import subprocess
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import sqlite3

class ImperialAlertSystem:
    def __init__(self, config_file='~/.imperial_alerts.json'):
        self.config_file = os.path.expanduser(config_file)
        self.load_config()
        self.init_database()
        
    def load_config(self):
        """Load or create alert configuration"""
        default_config = {
            "email": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "",
                "sender_password": "",
                "recipient_email": ""
            },
            "milestones": [
                {"value": 100, "label": "R100B", "message": "🚀 First 100B reached! Infrastructure scaling initiated."},
                {"value": 250, "label": "R250B", "message": "⚡ Halfway to sovereign goal! Network expanding rapidly."},
                {"value": 400, "label": "R400B", "message": "🏛️ Critical mass achieved. Final ascent to R500B."},
                {"value": 500, "label": "R500B", "message": "🎉 IMPERIAL OMEGA: SOVEREIGN GOAL ACHIEVED! 🎉"}
            ],
            "last_alerted": {}
        }
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()
            
    def save_config(self):
        """Save alert configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        os.chmod(self.config_file, 0o600)  # Secure file permissions
            
    def init_database(self):
        """Initialize SQLite database for alert history"""
        self.db_path = os.path.expanduser('~/imperial_network/alerts.db')
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS alerts
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      timestamp TEXT,
                      milestone REAL,
                      message TEXT,
                      sent INTEGER)''')
        c.execute('''CREATE TABLE IF NOT EXISTS metrics
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      timestamp TEXT,
                      valuation REAL,
                      villages INTEGER,
                      lithium_price REAL)''')
        conn.commit()
        conn.close()
        
    def get_current_valuation(self):
        """Fetch current valuation from Node-RED"""
        try:
            # Try to get from API
            result = subprocess.run(
                ['curl', '-s', '-X', 'POST', 'http://127.0.0.1:1880/village_data',
                 '-H', 'Content-Type: application/json',
                 '-d', '{"metric": "valuation"}'],
                capture_output=True, text=True
            )
            if result.stdout:
                data = json.loads(result.stdout)
                # Parse valuation (example: 269.9B -> 269.9)
                valuation = data.get('valuation', 269.9)
                return float(valuation)
        except:
            # Fallback to local metrics
            try:
                with open('/tmp/current_valuation.txt', 'r') as f:
                    return float(f.read().strip())
            except:
                return 269.9  # Default current valuation
        return 269.9
    
    def send_email_alert(self, milestone, message):
        """Send email alert for milestone"""
        if not self.config['email']['enabled']:
            print(f"📧 Email alert (disabled): {message}")
            return False
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['email']['sender_email']
            msg['To'] = self.config['email']['recipient_email']
            msg['Subject'] = f"🏛️ IMPERIAL OMEGA: {milestone} MILESTONE ACHIEVED!"
            
            body = f"""
            <html>
            <body style="font-family: monospace; background: #0a0a0f; color: #00ff00;">
                <div style="border: 2px solid #ffd700; padding: 20px; background: #1a1a2e;">
                    <h1 style="color: #ffd700;">🏛️ IMPERIAL OMEGA</h1>
                    <h2>🎯 MILESTONE: {milestone}</h2>
                    <p>{message}</p>
                    <hr>
                    <p>📊 Current Metrics:</p>
                    <ul>
                        <li>Valuation: {self.get_current_valuation()}B</li>
                        <li>Progress to R500B: {(self.get_current_valuation()/5):.1f}%</li>
                    </ul>
                    <p>📸 View dashboard: http://localhost:1880/ui</p>
                    <p><small>Imperial Sovereign Alert System | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(self.config['email']['smtp_server'], self.config['email']['smtp_port'])
            server.starttls()
            server.login(self.config['email']['sender_email'], self.config['email']['sender_password'])
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Email alert sent for {milestone}")
            return True
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False
    
    def check_milestones(self):
        """Check if any milestones have been reached"""
        current_val = self.get_current_valuation()
        
        for milestone in self.config['milestones']:
            milestone_val = milestone['value']
            milestone_key = str(milestone_val)
            
            # Check if milestone reached and not alerted
            if current_val >= milestone_val and milestone_key not in self.config.get('last_alerted', {}):
                # Send alert
                sent = self.send_email_alert(milestone['label'], milestone['message'])
                
                # Record in database
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                c.execute("INSERT INTO alerts (timestamp, milestone, message, sent) VALUES (?, ?, ?, ?)",
                         (datetime.now().isoformat(), milestone_val, milestone['message'], 1 if sent else 0))
                conn.commit()
                conn.close()
                
                # Update last alerted
                self.config.setdefault('last_alerted', {})[milestone_key] = datetime.now().isoformat()
                self.save_config()
                
                print(f"🎯 MILESTONE: {milestone['label']} reached at R{current_val}B!")
                
    def record_metrics(self):
        """Record current metrics to database for trend analysis"""
        current_val = self.get_current_valuation()
        
        # Try to get village count
        try:
            result = subprocess.run(
                ['curl', '-s', 'http://127.0.0.1:1880/village_data'],
                capture_output=True, text=True
            )
            data = json.loads(result.stdout) if result.stdout else {}
            villages = data.get('village_impact', {}).get('total_villages', 43)
            lithium = data.get('mineral_data', {}).get('lithium', {}).get('value', 'R4,200/t')
            # Parse lithium price (simple extraction)
            lithium_price = float(lithium.replace('R', '').replace('/t', '').replace(',', ''))
        except:
            villages = 43
            lithium_price = 4200
            
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO metrics (timestamp, valuation, villages, lithium_price) VALUES (?, ?, ?, ?)",
                 (datetime.now().isoformat(), current_val, villages, lithium_price))
        conn.commit()
        conn.close()
        
    def run(self):
        """Main alert system loop"""
        print("🏛️ Imperial Omega Alert System Activated")
        print("Monitoring for milestones...")
        
        while True:
            self.record_metrics()
            self.check_milestones()
            time.sleep(300)  # Check every 5 minutes

if __name__ == "__main__":
    alert_system = ImperialAlertSystem()
    alert_system.run()
