#!/usr/bin/env python3
from db_config import get_db_connection
"""
📡 NETWORK REVIVAL BROADCAST - Wake Up 100 Inactive Users
Uses Ukuvuselela Webhook (Port 8117)
"""
import sqlite3
import requests
import random
from datetime import datetime

print("📡 IMPERIAL NETWORK REVIVAL")
print("="*60)

conn = get_db_connection()
cursor = conn.cursor()

# Find 100 inactive users (users with no recent activity)
cursor.execute('''
    SELECT id, username, phone FROM users 
    WHERE id NOT IN (
        SELECT DISTINCT user_id FROM payment WHERE created_at > date('now', '-30 days')
    )
    AND phone IS NOT NULL AND phone != ''
    LIMIT 100
''')
inactive_users = cursor.fetchall()

print(f"\n👥 Found {len(inactive_users)} inactive users to revive")

# Send revival signal via USSD gateway (Port 8087)
revived = 0
for user_id, username, phone in inactive_users:
    try:
        # Send USSD revival message
        message = f"🏛️ Imperial Network: Your presence is requested. The empire grows to 1000. Reply to confirm sovereignty."
        response = requests.post(
            'http://localhost:8087/api/send_ussd',
            json={'phone': phone, 'message': message},
            timeout=3
        )
        if response.status_code == 200:
            revived += 1
            print(f"  ✅ Revival signal sent to {username} ({phone})")
    except:
        print(f"  ⚠️ Failed to reach {username} ({phone})")

print(f"\n📊 REVIVAL SUMMARY:")
print(f"   • Signals sent: {revived}/{len(inactive_users)}")
print(f"   • Target: 100 users to reach 1,000")
print(f"   • Current: 900 + {revived} = {900 + revived}")

# Log the revival
with open('logs/network_revival.log', 'a') as f:
    f.write(f"{datetime.now()}: Revival broadcast sent to {revived} users\n")

conn.close()
print("\n✅ Network revival complete")
