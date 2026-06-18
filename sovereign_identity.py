#!/usr/bin/env python3
from db_config import get_db_connection
"""
Sovereign Identity Card - Humbulani Mudau
"""
import sqlite3
from datetime import datetime

conn = get_db_connection()
cursor = conn.cursor()

print("🏛️ SOVEREIGN IMPERIAL IDENTITY CARD")
print("=" * 60)

# Your info
cursor.execute('''
    SELECT id, username, role, phone, village, created_at 
    FROM user WHERE username='humbulani_mudau'
''')
you = cursor.fetchone()

if you:
    print(f"""
    👑 SOVEREIGN: {you[1]}
    ━━━━━━━━━━━━━━━━━━━
    📋 ID:         {you[0]}
    🎭 Role:       {you[2].upper()}
    📱 Phone:      {you[3]}
    📍 Village:    {you[4]}
    ⏰ Joined:     {you[5][:10]} at {you[5][11:19]}
    """)

# Your village stats
cursor.execute('''
    SELECT COUNT(*) FROM user WHERE village='thohoyandou'
''')
thoyo_count = cursor.fetchone()[0]

cursor.execute('''
    SELECT COUNT(*) FROM user WHERE village='thohoyandou' AND role='sovereign'
''')
thoyo_sovereigns = cursor.fetchone()[0]

print(f"    🏘️  Thohoyandou Village: {thoyo_count} residents")
print(f"    👑 Sovereigns in village: {thoyo_sovereigns} (that's you!)")

# Network position
cursor.execute('SELECT COUNT(*) FROM user')
total = cursor.fetchone()[0]
print(f"\n    📊 You are user #{you[0]} of {total} in the Imperial Network")

# Recent activity in your village
cursor.execute('''
    SELECT username, created_at FROM user 
    WHERE village='thohoyandou' 
    ORDER BY id DESC LIMIT 3
''')
recent = cursor.fetchall()
print("\n    🆕 Recent Thohoyandou joins:")
for username, created in recent:
    print(f"       • {username} ({created[:10]})")

conn.close()
print("\n" + "=" * 60)
