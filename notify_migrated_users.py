#!/usr/bin/env python3
from db_config import get_db_connection
"""
Send notification to newly migrated users
"""
import sqlite3
from datetime import datetime

print("🏛️ NOTIFYING MIGRATED USERS")
print("=" * 60)

conn = get_db_connection()
cursor = conn.cursor()

# Get users migrated today (or recently)
cursor.execute('''
    SELECT username, phone, village FROM user 
    WHERE created_at > datetime('now', '-1 hour')
    ORDER BY id DESC
''')

users = cursor.fetchall()
print(f"📢 Found {len(users)} recently migrated users")

for user in users:
    username, phone, village = user
    print(f"   📱 {username} ({phone}) - {village}")
    # In production, you'd send actual notifications here
    # requests.post("http://localhost:8087/api/notify", json={"phone": phone, "message": "Welcome to Imperial Network!"})

print("\n✅ Notification simulation complete")
conn.close()
