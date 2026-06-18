#!/usr/bin/env python3
from db_config import get_db_connection
"""
📉 WAR-PRICE INDEX - Economic Early Warning
Port 8103 (Intel Alpha)
Monitors fuel prices, exchange rates, and gold for war indicators
"""
import requests
import json
import time
import sqlite3
from datetime import datetime
import os

class EconomicMonitor:
    def __init__(self):
        self.log_file = "logs/economic_monitor.log"
        os.makedirs("logs", exist_ok=True)
        
        # Thresholds
        self.thresholds = {
            'diesel_increase': 1.50,  # R1.50/liter increase = hoarding/panic
            'zar_usd': 20.50,          # ZAR/USD > 20.50 = capital flight
            'gold_price': 2800,         # Gold > R2800/g = safe haven movement
            'oil_price': 140,           # Brent Crude > $140 = global shock
            'fuel_daily_jump': 0.08     # 8% daily fuel jump = panic
        }
        
        # Baseline values (would be fetched from APIs in production)
        self.baselines = {
            'diesel': 23.50,
            'zar_usd': 18.20,
            'gold': 2652,
            'oil': 85,
            'last_fuel_price': 23.50,
            'fuel_check_time': datetime.now()
        }
    
    def fetch_diesel_price(self):
        """Fetch local diesel price from API"""
        # In production, would hit SAPIA or fuel API
        # Simulated for demo
        import random
        # Random fluctuation within 2%
        fluctuation = random.uniform(-0.02, 0.05)
        return self.baselines['diesel'] * (1 + fluctuation)
    
    def fetch_exchange_rate(self):
        """Fetch ZAR/USD exchange rate"""
        # Simulated
        import random
        fluctuation = random.uniform(-0.03, 0.04)
        return self.baselines['zar_usd'] * (1 + fluctuation)
    
    def fetch_gold_price(self):
        """Fetch gold price in ZAR/g"""
        # Simulated
        import random
        fluctuation = random.uniform(-0.01, 0.03)
        return self.baselines['gold'] * (1 + fluctuation)
    
    def fetch_oil_price(self):
        """Fetch Brent Crude price in USD"""
        # Simulated
        import random
        fluctuation = random.uniform(-0.02, 0.04)
        return self.baselines['oil'] * (1 + fluctuation)
    
    def log_status(self, level, message):
        """Log to file and console"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {level}: {message}"
        
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
            ''', ('economic_status', 
                  1 if '🔴' in level else 0.5 if '🟡' in level else 0, 
                  message, 
                  datetime.now().isoformat()))
            conn.commit()
            conn.close()
        except:
            pass
    
    def check_economic_war(self):
        """Check all indicators for war signals"""
        diesel = self.fetch_diesel_price()
        exchange = self.fetch_exchange_rate()
        gold = self.fetch_gold_price()
        oil = self.fetch_oil_price()
        
        alerts = []
        warning_level = "🟢 STABLE"
        
        # Check diesel surge (hoarding/panic)
        diesel_increase = diesel - self.baselines['diesel']
        if diesel_increase > self.thresholds['diesel_increase']:
            alerts.append(f"DIESEL SURGE: +R{diesel_increase:.2f}/L")
            warning_level = "🟡 WARNING"
        
        # Check daily fuel jump percentage
        if self.baselines['last_fuel_price'] > 0:
            daily_jump = (diesel - self.baselines['last_fuel_price']) / self.baselines['last_fuel_price']
            if daily_jump > self.thresholds['fuel_daily_jump']:
                alerts.append(f"FUEL PANIC: +{daily_jump*100:.1f}% in 24h")
                warning_level = "🔴 CRITICAL"
        
        # Update baseline for next check
        if (datetime.now() - self.baselines['fuel_check_time']).days >= 1:
            self.baselines['last_fuel_price'] = diesel
            self.baselines['fuel_check_time'] = datetime.now()
        
        # Check exchange rate (capital flight)
        if exchange > self.thresholds['zar_usd']:
            alerts.append(f"ZAR COLLAPSE: R{exchange:.2f}/USD")
            warning_level = "🔴 CRITICAL"
        
        # Check gold (safe haven)
        if gold > self.thresholds['gold_price']:
            alerts.append(f"GOLD RUSH: R{gold:.0f}/g")
            warning_level = "🟡 WARNING"
        
        # Check oil (global shock)
        if oil > self.thresholds['oil_price']:
            alerts.append(f"OIL SHOCK: ${oil:.1f}/barrel")
            warning_level = "🔴 CRITICAL"
        
        return warning_level, alerts, {
            'diesel': diesel,
            'exchange': exchange,
            'gold': gold,
            'oil': oil
        }
    
    def run(self):
        """Main monitoring loop"""
        self.log_status("🟢 INIT", "Economic Monitor active on Port 8103")
        self.log_status("📊 THRESHOLDS", str(self.thresholds))
        
        while True:
            try:
                level, alerts, values = self.check_economic_war()
                
                if alerts:
                    alert_msg = f"{level} | " + " | ".join(alerts)
                    self.log_status(level, alert_msg)
                    
                    # Send SMS for critical alerts
                    if "🔴" in level:
                        try:
                            import requests
                            requests.post('http://localhost:8087/api/send_sms', 
                                         json={'phone': '0794658481', 'message': alert_msg},
                                         timeout=2)
                        except:
                            pass
                else:
                    self.log_status(level, f"Diesel: R{values['diesel']:.2f} | USD: R{values['exchange']:.2f} | Gold: R{values['gold']:.0f} | Oil: ${values['oil']:.1f}")
                
                time.sleep(900)  # Check every 15 minutes
                
            except KeyboardInterrupt:
                self.log_status("🛑 TERM", "Economic Monitor shutting down")
                break
            except Exception as e:
                self.log_status("❌ ERROR", str(e))
                time.sleep(60)

if __name__ == "__main__":
    monitor = EconomicMonitor()
    monitor.run()
