#!/usr/bin/env python3
from db_config import get_db_connection
"""
🔔 IMPERIAL MILESTONE ALERT - Family Dividend Tracker
Monitors Sovereign Pocket growth and logs R10k milestones
"""
import sqlite3
import os
from datetime import datetime

def check_milestone():
    print("🔔 IMPERIAL MILESTONE ALERT")
    print("="*60)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check current available CEO funds
    cursor.execute("SELECT SUM(ceo_cut_2_percent) FROM ceo_pocket WHERE status='available'")
    available = cursor.fetchone()[0] or 0
    
    # Get breakdown by source
    cursor.execute("SELECT source_sector, SUM(ceo_cut_2_percent) FROM ceo_pocket WHERE status='available' GROUP BY source_sector")
    breakdown = cursor.fetchall()
    
    # Calculate milestones
    milestones = int(available // 10000)
    next_milestone = (milestones + 1) * 10000
    remaining = next_milestone - available
    
    # Get last milestone logged
    log_file = os.path.expanduser('~/imperial_vault/family_dividends.log')
    last_milestone = 0
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            lines = f.readlines()
            if lines:
                for line in reversed(lines):
                    if 'Milestone' in line:
                        try:
                            last_milestone = int(line.split('Milestone')[1].split(':')[0].strip())
                            break
                        except:
                            pass
    
    print(f"\n📊 SOVEREIGN POCKET STATUS")
    print(f"  💰 Total Available: R{available:,.2f}")
    print(f"  🎯 Milestones Reached: {milestones} x R10,000")
    print(f"  🏁 Next Milestone: R{next_milestone:,.2f} (R{remaining:,.2f} to go)")
    
    print(f"\n📋 BREAKDOWN BY SOURCE:")
    for source, amount in breakdown:
        print(f"  • {source}: R{amount:,.2f}")
    
    # Log new milestones
    if milestones > last_milestone:
        with open(log_file, 'a') as f:
            f.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔔 MILESTONE ACHIEVED!\n")
            f.write(f"   • Milestone #{milestones}: R{available:,.2f}\n")
            for source, amount in breakdown:
                f.write(f"   • {source}: R{amount:,.2f}\n")
            f.write(f"   • Next: R{next_milestone:,.2f} (R{remaining:,.2f} away)\n")
            f.write("-" * 60 + "\n")
        
        print(f"\n✅ NEW MILESTONE #{milestones} LOGGED!")
    
    # Show family summary
    print(f"\n🏠 FAMILY SUMMARY:")
    print(f"  • Daily Family Budget: R{available/30:,.2f}/day")
    print(f"  • Monthly Family Fund: R{available/12:,.2f}/month")
    print(f"  • School Fees Covered: {available // 20000} terms")
    
    # Check if we should trigger SMS alert
    if remaining < 1000:
        try:
            import requests
            phone = "0794658481"
            message = f"🏛️ IMPERIAL ALERT: Only R{remaining:,.2f} to next R10k milestone! Current pocket: R{available:,.2f}"
            requests.post('http://localhost:8087/api/send_sms', 
                         json={'phone': phone, 'message': message},
                         timeout=2)
            print(f"  📱 SMS alert sent: {message}")
        except:
            pass
    
    conn.close()
    print("\n✅ Milestone check complete")

if __name__ == "__main__":
    check_milestone()
