#!/usr/bin/env python3
from db_config import get_db_connection
"""
📝 CEO WITHDRAWAL SLIP - Proof of Income Generator
"""
import sqlite3
from datetime import datetime
import os

print("📝 IMPERIAL WITHDRAWAL SLIP")
print("="*60)

conn = get_db_connection()
cursor = conn.cursor()

# Get available CEO funds
cursor.execute("SELECT SUM(ceo_cut_2_percent) FROM ceo_pocket WHERE status='available'")
available = cursor.fetchone()[0] or 0

# Get breakdown
cursor.execute("SELECT source_sector, ceo_cut_2_percent FROM ceo_pocket WHERE status='available'")
breakdown = cursor.fetchall()

print(f"\n👑 SOVEREIGN: Humbulani Mudau")
print(f"📅 DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"💰 TOTAL AVAILABLE: R{available:,.2f}")
print("\n" + "="*60)
print("WITHDRAWAL SLIP")
print("="*60)

slip_number = f"IMP-WD-{datetime.now().strftime('%Y%m%d')}-{hash(datetime.now()) % 10000:04d}"

print(f"\nSLIP NO: {slip_number}")
print(f"AMOUNT: R{available:,.2f}")
print("\nBREAKDOWN:")
for sector, amount in breakdown:
    print(f"  • {sector}: R{amount:,.2f}")

print("\n" + "="*60)
print("CERTIFICATION")
print("="*60)
print("""
This certifies that the above amount represents
the Sovereign's 2% Management Fee from Imperial
Network operations. Funds are available for
immediate withdrawal to the family account.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IMPERIAL NETWORK - FOUNDER'S FEE
CIPC: 2026/1730663/07
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

# Save to vault
filename = f"~/imperial_vault/withdrawal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
with open(os.path.expanduser(filename), 'w') as f:
    f.write(f"IMPERIAL WITHDRAWAL SLIP\n")
    f.write(f"Sovereign: Humbulani Mudau\n")
    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Amount: R{available:,.2f}\n")
    f.write(f"Slip No: {slip_number}\n")
    f.write(f"Source: 2% Management Fee\n")
    f.write(f"CIPC: 2026/1730663/07\n")

print(f"✅ Slip saved to: {filename}")

# Option to mark as withdrawn
print(f"\n💳 MARK AS WITHDRAWN? (yes/no)")
choice = input("> ").strip().lower()
if choice == 'yes':
    cursor.execute("UPDATE ceo_pocket SET status='withdrawn' WHERE status='available'")
    conn.commit()
    print(f"✅ Funds marked as withdrawn. Receipt saved for tax purposes.")
else:
    print(f"ℹ️ Funds remain available.")

conn.close()
