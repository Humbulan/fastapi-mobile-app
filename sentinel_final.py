#!/usr/bin/env python3
from db_config import get_db_connection
"""
👑 IMPERIAL SOVEREIGN SENTINEL - FINAL VERSION
"""
import os
import sqlite3
from datetime import datetime

# Load .env file manually
env_file = os.path.expanduser('~/imperial_network/.env')
if os.path.exists(env_file):
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value.strip('"').strip("'")

print("📊 SOVEREIGN DASHBOARD ACCESS")
print("-" * 40)

# Get credentials
user = os.getenv('IMPERIAL_USER', 'Humbulani_Mudau')
key = os.getenv('IMPERIAL_KEY', 'PREMIUM_KEY_A1B2C3D4')

print(f"👑 Identity: {user}")
print(f"🔑 Key: {key[:8]}... (secured)")

# Connect to database
conn = get_db_connection()
c = conn.cursor()

# Get SADC pending
c.execute("SELECT SUM(amount) FROM payment WHERE payment_method LIKE 'SADC%' AND status='pending'")
sadc_total = c.fetchone()[0] or 0

# Get web upgrade capital
c.execute("SELECT SUM(amount) FROM payment WHERE payment_method='IMPERIAL_WEB_UPGRADE'")
web_total = c.fetchone()[0] or 0

# Get IDC sectors
c.execute("SELECT SUM(amount) FROM payment WHERE payment_method='SADC_A_LOGISTICS'")
sadc_a = c.fetchone()[0] or 0
c.execute("SELECT SUM(amount) FROM payment WHERE payment_method='SADC_B_RETAIL'")
sadc_b = c.fetchone()[0] or 0

# Get users
c.execute("SELECT COUNT(*) FROM users")
users = c.fetchone()[0]

conn.close()

# Display results
print(f"\n💰 SADC CORRIDOR PENDING: R{sadc_total:,.2f}")
print(f"   • SADC_A_LOGISTICS:    R{sadc_a:,.2f}")
print(f"   • SADC_B_RETAIL:       R{sadc_b:,.2f}")
print(f"🌐 WEB UPGRADE CAPITAL:   R{web_total:,.2f}")
print(f"👥 ACTIVE SOVEREIGNS:     {users}")
print(f"💎 TOTAL IMPERIAL WEALTH: R{sadc_total + web_total:,.2f}")
print(f"\n👑 CEO: {user}")
print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
