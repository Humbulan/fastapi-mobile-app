#!/usr/bin/env python3
from db_config import get_db_connection
"""
Sovereign Dashboard - Imperial Network Overview
"""
import sqlite3
from datetime import datetime

print("🏛️ SOVEREIGN IMPERIAL DASHBOARD")
print("=" * 60)
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

conn = get_db_connection()
cursor = conn.cursor()

# Total users
cursor.execute("SELECT COUNT(*) FROM users")
total_users = cursor.fetchone()[0]
print(f"👥 Total Users: {total_users}")

# Users by role
cursor.execute("SELECT role, COUNT(*) FROM users GROUP BY role")
roles = cursor.fetchall()
print("\n📊 Users by Role:")
for role, count in roles:
    print(f"   {role}: {count}")

# Users by village (top 10)
cursor.execute("SELECT village, COUNT(*) FROM users WHERE village IS NOT NULL AND village != '' GROUP BY village ORDER BY COUNT(*) DESC LIMIT 10")
villages = cursor.fetchall()
print("\n📍 Top Villages:")
for village, count in villages:
    print(f"   {village}: {count}")

# Recently added
cursor.execute("SELECT username, village, created_at FROM users ORDER BY id DESC LIMIT 5")
recent = cursor.fetchall()
print("\n🆕 Recently Added:")
for username, village, created in recent:
    print(f"   {username} - {village} ({created[:10]})")

# Sovereign info
cursor.execute("SELECT username, phone, village FROM users WHERE role='sovereign'")
sovereigns = cursor.fetchall()
print("\n👑 Sovereigns:")
for username, phone, village in sovereigns:
    print(f"   {username} ({phone}) - {village}")

conn.close()
print("\n" + "=" * 60)
