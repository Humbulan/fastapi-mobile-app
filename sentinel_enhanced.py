#!/usr/bin/env python3
from db_config import get_db_connection
"""
🛡️ IMPERIAL SENTINEL ENHANCED - With Alerts
Monitors SADC/Mobile balance and sends notifications
"""
import sqlite3
import json
import time
import requests
from datetime import datetime
from pathlib import Path

class ImperialSentinel:
    def __init__(self):
        self.db_path = 'instance/imperial.db'
        self.thresholds = {
            'sadc_growth': 0.15,      # 15% growth alert
            'mobile_growth': 0.30,     # 30% growth alert
            'sadc_ratio_min': 0.95,    # Minimum 95% SADC ratio
            'sadc_ratio_max': 1.0    # Maximum 99.5% SADC ratio
        }
        self.history = []
        self.alert_log = Path('logs/sentinel_alerts.log')
        self.alert_log.parent.mkdir(exist_ok=True)
        
    def analyze_current(self):
        """Get current transaction distribution"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN payment_method LIKE 'SADC%' THEN 'SADC_TRADE'
                    WHEN payment_method IN ('mtn_momo', 'mobile_money') THEN 'MOBILE_PAYMENTS'
                    ELSE 'OTHER'
                END as category,
                COUNT(*) as tx_count,
                SUM(amount) as total
            FROM payment
            WHERE status IN ('pending', 'completed')
            GROUP BY category
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        current = {
            'timestamp': datetime.now().isoformat(),
            'categories': {}
        }
        
        for cat, count, total in results:
            current['categories'][cat] = {
                'count': count,
                'total': total or 0
            }
        
        return current
    
    def send_alert(self, alert):
        """Send alert via USSD/email"""
        # Log to file
        with open(self.alert_log, 'a') as f:
            f.write(f"{alert['timestamp']} | {alert['level']} | {alert['message']}\n")
        
        # Print to console
        print(f"\n⚠️ {alert['level']}: {alert['message']}")
        
        # Send SMS via USSD gateway if available
        try:
            phone = "0794658481"  # Your number
            message = f"IMPERIAL ALERT: {alert['message']}"
            requests.post('http://localhost:8087/api/send_sms', 
                         json={'phone': phone, 'message': message},
                         timeout=2)
        except:
            pass
    
    def check_alerts(self, current):
        """Check for threshold violations"""
        alerts = []
        
        sadc = current['categories'].get('SADC_TRADE', {'count': 0, 'total': 0})
        mobile = current['categories'].get('MOBILE_PAYMENTS', {'count': 0, 'total': 0})
        total = sadc['total'] + mobile['total']
        
        # Check ratio
        if total > 0:
            sadc_ratio = sadc['total'] / total
            if sadc_ratio < self.thresholds['sadc_ratio_min']:
                alerts.append({
                    'level': 'CRITICAL',
                    'message': f"SADC ratio dropped to {sadc_ratio:.2%} (below {self.thresholds['sadc_ratio_min']:.0%})",
                    'timestamp': current['timestamp']
                })
            elif sadc_ratio > self.thresholds['sadc_ratio_max']:
                alerts.append({
                    'level': 'INFO',
                    'message': f"SADC ratio at {sadc_ratio:.2%} - Mobile payments low",
                    'timestamp': current['timestamp']
                })
        
        # Compare with last reading
        if self.history:
            last = self.history[-1]
            last_sadc = last['categories'].get('SADC_TRADE', {'total': 0})['total']
            last_mobile = last['categories'].get('MOBILE_PAYMENTS', {'total': 0})['total']
            
            if last_sadc > 0:
                sadc_growth = (sadc['total'] - last_sadc) / last_sadc
                if abs(sadc_growth) > self.thresholds['sadc_growth']:
                    alerts.append({
                        'level': 'WARNING',
                        'message': f"SADC {'+' if sadc_growth>0 else '-'}{abs(sadc_growth):.2%} change",
                        'timestamp': current['timestamp']
                    })
            
            if last_mobile > 0:
                mobile_growth = (mobile['total'] - last_mobile) / last_mobile
                if abs(mobile_growth) > self.thresholds['mobile_growth']:
                    alerts.append({
                        'level': 'NOTICE',
                        'message': f"Mobile payments {'+' if mobile_growth>0 else '-'}{abs(mobile_growth):.2%} change",
                        'timestamp': current['timestamp']
                    })
        
        return alerts
    
    def display_status(self, current, alerts):
        """Display current status"""
        sadc = current['categories'].get('SADC_TRADE', {'total': 0, 'count': 0})
        mobile = current['categories'].get('MOBILE_PAYMENTS', {'total': 0, 'count': 0})
        
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] IMPERIAL STATUS")
        print(f"  🌍 SADC:      R{sadc['total']/1e9:.2f}B ({sadc['count']} TX)")
        print(f"  📱 Mobile:    R{mobile['total']/1e6:.2f}M ({mobile['count']} TX)")
        print(f"  💎 Total:     R{(sadc['total']+mobile['total'])/1e9:.2f}B")
        
        if alerts:
            for alert in alerts:
                print(f"  ⚠️ {alert['level']}: {alert['message']}")
                self.send_alert(alert)
        else:
            print(f"  ✅ All thresholds normal")
    
    def run(self, interval=60):
        """Run continuous monitoring"""
        print("🛡️ IMPERIAL SENTINEL ENHANCED - ACTIVE")
        print("="*60)
        print(f"Monitoring interval: {interval}s")
        print(f"SADC growth threshold: {self.thresholds['sadc_growth']:.0%}")
        print(f"Mobile growth threshold: {self.thresholds['mobile_growth']:.0%}")
        print(f"SADC ratio range: {self.thresholds['sadc_ratio_min']:.0%} - {self.thresholds['sadc_ratio_max']:.0%}")
        print("="*60)
        
        try:
            while True:
                current = self.analyze_current()
                self.history.append(current)
                
                # Keep last 10 readings
                if len(self.history) > 10:
                    self.history.pop(0)
                
                alerts = self.check_alerts(current)
                self.display_status(current, alerts)
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n🛡️ Sentinel shutting down")
            print(f"📊 Final stats logged to: {self.alert_log}")
    
    def report(self):
        """Generate one-time report"""
        current = self.analyze_current()
        sadc = current['categories'].get('SADC_TRADE', {'total': 0, 'count': 0})
        mobile = current['categories'].get('MOBILE_PAYMENTS', {'total': 0, 'count': 0})
        
        print("\n📊 IMPERIAL SENTINEL REPORT")
        print("="*60)
        print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print(f"🌍 SADC TRADE")
        print(f"   Transactions: {sadc['count']}")
        print(f"   Total Value: R{sadc['total']:,.2f}")
        print(f"   Share: {sadc['total']/(sadc['total']+mobile['total'])*100:.1f}%")
        print()
        print(f"📱 MOBILE PAYMENTS")
        print(f"   Transactions: {mobile['count']}")
        print(f"   Total Value: R{mobile['total']:,.2f}")
        print(f"   Share: {mobile['total']/(sadc['total']+mobile['total'])*100:.1f}%")
        print()
        print(f"💎 TOTAL SYSTEM: R{sadc['total']+mobile['total']:,.2f}")
        print("="*60)
        
        # Save report
        report_file = f"logs/sentinel_report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(current, f, indent=2)
        print(f"📁 Report saved to: {report_file}")

if __name__ == "__main__":
    import sys
    sentinel = ImperialSentinel()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--report':
            sentinel.report()
        elif sys.argv[1] == '--once':
            current = sentinel.analyze_current()
            alerts = sentinel.check_alerts(current)
            sentinel.display_status(current, alerts)
    else:
        sentinel.run()
