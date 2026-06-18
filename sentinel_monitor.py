#!/usr/bin/env python3
from db_config import get_db_connection
"""
🛡️ IMPERIAL SENTINEL - Real-time Topic Cluster Monitor
Alerts when SADC/Mobile balance shifts unexpectedly
"""
import sqlite3
import json
import time
from datetime import datetime
from collections import defaultdict

class ImperialSentinel:
    def __init__(self):
        self.db_path = 'instance/imperial.db'
        self.thresholds = {
            'sadc_growth': 0.15,      # 15% growth alert
            'mobile_growth': 0.30,     # 30% growth alert
            'sadc_ratio': 0.95         # 95% of total is normal
        }
        self.history = []
        
    def analyze_current(self):
        """Get current transaction distribution"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Count SADC vs Mobile payments
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
    
    def check_alerts(self, current):
        """Check for threshold violations"""
        alerts = []
        
        sadc = current['categories'].get('SADC_TRADE', {'count': 0, 'total': 0})
        mobile = current['categories'].get('MOBILE_PAYMENTS', {'count': 0, 'total': 0})
        total = sadc['total'] + mobile['total']
        
        # Check ratio
        if total > 0:
            sadc_ratio = sadc['total'] / total
            if sadc_ratio < self.thresholds['sadc_ratio']:
                alerts.append({
                    'level': 'WARNING',
                    'message': f"SADC ratio dropped to {sadc_ratio:.2%}",
                    'threshold': f"{self.thresholds['sadc_ratio']:.0%}"
                })
        
        # Compare with last reading
        if self.history:
            last = self.history[-1]
            last_sadc = last['categories'].get('SADC_TRADE', {'total': 0})['total']
            last_mobile = last['categories'].get('MOBILE_PAYMENTS', {'total': 0})['total']
            
            if last_sadc > 0:
                sadc_growth = (sadc['total'] - last_sadc) / last_sadc
                if sadc_growth > self.thresholds['sadc_growth']:
                    alerts.append({
                        'level': 'INFO',
                        'message': f"SADC growth: +{sadc_growth:.2%}",
                        'amount': f"R{sadc['total'] - last_sadc:,.2f}"
                    })
            
            if last_mobile > 0:
                mobile_growth = (mobile['total'] - last_mobile) / last_mobile
                if mobile_growth > self.thresholds['mobile_growth']:
                    alerts.append({
                        'level': 'NOTICE',
                        'message': f"Mobile payments grew +{mobile_growth:.2%}",
                        'amount': f"R{mobile['total'] - last_mobile:,.2f}"
                    })
        
        return alerts
    
    def run(self, interval=60):
        """Run continuous monitoring"""
        print("🛡️ IMPERIAL SENTINEL ACTIVE")
        print("="*50)
        print(f"Monitoring interval: {interval}s")
        print(f"SADC growth threshold: {self.thresholds['sadc_growth']:.0%}")
        print(f"Mobile growth threshold: {self.thresholds['mobile_growth']:.0%}")
        print("="*50)
        
        try:
            while True:
                current = self.analyze_current()
                self.history.append(current)
                
                # Keep last 10 readings
                if len(self.history) > 10:
                    self.history.pop(0)
                
                alerts = self.check_alerts(current)
                
                # Display status
                sadc = current['categories'].get('SADC_TRADE', {'total': 0})
                mobile = current['categories'].get('MOBILE_PAYMENTS', {'total': 0})
                
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] IMPERIAL STATUS")
                print(f"  🌍 SADC:      R{sadc['total']/1e9:.2f}B ({sadc.get('count', 0)} TX)")
                print(f"  📱 Mobile:    R{mobile['total']/1e6:.2f}M ({mobile.get('count', 0)} TX)")
                
                if alerts:
                    for alert in alerts:
                        print(f"  ⚠️ {alert['level']}: {alert['message']}")
                else:
                    print("  ✅ All thresholds normal")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n🛡️ Sentinel shutting down")
    
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

if __name__ == "__main__":
    import sys
    sentinel = ImperialSentinel()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--report':
        sentinel.report()
    else:
        sentinel.run()
