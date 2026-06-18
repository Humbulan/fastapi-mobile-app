#!/usr/bin/env python3
from db_config import get_db_connection
"""
Council PIN Dashboard - Imperial Network
"""
import sqlite3
from datetime import datetime

print("🏛️ IMPERIAL COUNCIL DASHBOARD")
print("=" * 60)
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

conn = get_db_connection()
cursor = conn.cursor()

# Basic stats
cursor.execute("SELECT COUNT(*) FROM council_pins")
total_members = cursor.fetchone()[0]

cursor.execute("SELECT SUM(allocation) FROM council_pins")
total_fund = cursor.fetchone()[0] or 0

cursor.execute("SELECT COUNT(*) FROM council_pins WHERE status='active'")
active_members = cursor.fetchone()[0]

print(f"👥 Council Members: {total_members}")
print(f"💰 Total Fund: R{total_fund:,.2f}")
print(f"✨ With Alpha (1.25x): R{total_fund * 1.25:,.2f}")
print(f"✅ Active Members: {active_members}")

# Distribution by phone suffix range
print("\n📊 Distribution by Phone Suffix Range:")
cursor.execute('''
    SELECT 
        CASE 
            WHEN phone_suffix BETWEEN '6000' AND '6099' THEN '6000-6099'
            WHEN phone_suffix BETWEEN '6100' AND '6199' THEN '6100-6199'
            ELSE 'Other'
        END as range,
        COUNT(*) as count
    FROM council_pins
    GROUP BY range
    ORDER BY range
''')
ranges = cursor.fetchall()
for range_name, count in ranges:
    print(f"   {range_name}: {count} members")

# Recent allocations (first 10 by ID)
print("\n📋 Council Members (first 10):")
cursor.execute('''
    SELECT member_id, phone_suffix, pin, allocation, status 
    FROM council_pins 
    ORDER BY member_id 
    LIMIT 10
''')
members = cursor.fetchall()
for member in members:
    status_marker = "✅" if member[4] == 'active' else "⏸️"
    print(f"   {status_marker} {member[0]}: PIN {member[2]} - R{member[3]} ({member[1]})")

# Summary
print("\n" + "=" * 60)
print(f"🏛️ Total Council Value: R{total_fund:,.2f}")
print(f"⚡ After Alpha Boost: R{total_fund * 1.25:,.2f}")
print("=" * 60)

conn.close()
