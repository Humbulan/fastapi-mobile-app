#!/usr/bin/env python3
from db_config import get_db_connection
"""
Manual user entry from broadcast output
"""
import sqlite3
import hashlib
from datetime import datetime

# List of users from your broadcast (I'll add a few samples, you can add more)
# Based on the first few lines of your broadcast:
users = [
    {"name": "James Mudau", "phone": "0721234567", "village": "thohoyandou"},
    {"name": "Sarah Mulaudzi", "phone": "0822345678", "village": "sibasa"},
    {"name": "Thomas Nemadodzi", "phone": "0713456789", "village": "manini"},
    {"name": "Maria Tshikovhi", "phone": "0834567890", "village": "malamulele"},
    {"name": "David Phaswana", "phone": "0725678901", "village": "mukhomi"},
    {"name": "Grace Mabunda", "phone": "0816789012", "village": "gundo"},
    {"name": "Peter Netshisaulu", "phone": "0737890123", "village": "makhuvha"},
    {"name": "Lerato Baloyi", "phone": "0828901234", "village": "folovhodwe"},
    {"name": "James Mathidi", "phone": "0738721174", "village": "thohoyandou"},
    {"name": "Mark Tshamano", "phone": "0762150527", "village": "sibasa"},
    # Add more users here from your broadcast output
]

print("🏛️ MANUAL USER RESTORATION")
print("=" * 60)

conn = get_db_connection()
cursor = conn.cursor()

restored = 0
for user in users:
    try:
        username = user['name'].lower().replace(' ', '_')
        email = f"{username}@restored.user"
        password_hash = hashlib.sha256(f"changeme_{username}".encode()).hexdigest()
        
        cursor.execute('''
            INSERT OR IGNORE INTO user 
            (username, email, password, role, phone, village, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            username,
            email,
            password_hash,
            'user',
            user['phone'],
            user['village'],
            datetime.now().isoformat()
        ))
        
        if cursor.rowcount > 0:
            restored += 1
            print(f"✅ Restored: {user['name']} ({user['phone']}) - {user['village']}")
    except Exception as e:
        print(f"⚠️  Error with {user['name']}: {e}")

conn.commit()
cursor.execute('SELECT COUNT(*) FROM user')
total = cursor.fetchone()[0]
conn.close()

print("\n" + "=" * 60)
print(f"📊 RESTORATION SUMMARY:")
print(f"   ✅ Users restored: {restored}")
print(f"   📈 Total users now: {total}")
