#!/usr/bin/env python3
from db_config import get_db_connection
"""
📱 USSD DAWN REPORT - Mobile Command Version
"""
import sqlite3
from datetime import datetime

print("Content-Type: text/plain\n")
print("🏛️ IMPERIAL OMEGA")
print("=" * 30)

conn = get_db_connection()
c = conn.cursor()

# Port status
c.execute("SELECT COUNT(*) FROM system_sectors WHERE status='online'")
online = c.fetchone()[0]
print(f"📊 PORTS: {online}/46")

# Users
c.execute("SELECT COUNT(*) FROM users")
users = c.fetchone()[0]
print(f"👥 USERS: {users}")

# SADC Pending
c.execute("SELECT SUM(amount) FROM payment WHERE payment_method LIKE 'SADC%' AND status='pending'")
sadc = c.fetchone()[0] or 0
print(f"🚀 SADC: R{sadc/1e9:.1f}B")

# Wealth Lock
c.execute("SELECT true_valuation FROM wealth_tracking WHERE id=1")
wealth = c.fetchone()[0] or 0
print(f"💎 LOCKED: R{wealth/1e9:.1f}B")

conn.close()
print("=" * 30)
print(f"👑 CEO: Humbulani Mudau")
print(f"🕒 {datetime.now().strftime('%H:%M')}")
