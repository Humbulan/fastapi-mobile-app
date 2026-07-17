#!/usr/bin/env python3
from db_config import get_db_connection
"""
🏛️ FINAL IMPERIAL DASHBOARD - COMPLETE SYSTEM STATUS
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path

print("🏛️ IMPERIAL NETWORK - FINAL SOVEREIGN DASHBOARD")
print("=" * 70)
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Connect to Imperial DB
conn = get_db_connection()
cursor = conn.cursor()

# SECTION 1: USER STATS
print("👥 USER STATISTICS")
print("-" * 40)
cursor.execute('SELECT COUNT(*) FROM user')
total_users = cursor.fetchone()[0]
cursor.execute('SELECT role, COUNT(*) FROM user GROUP BY role')
roles = cursor.fetchall()
print(f"Total Users: {total_users}")
for role, count in roles:
    print(f"  {role}: {count}")

cursor.execute('SELECT village, COUNT(*) FROM user WHERE village IS NOT NULL AND village != "" GROUP BY village ORDER BY COUNT(*) DESC LIMIT 5')
top_villages = cursor.fetchall()
print("\nTop 5 Villages:")
for village, count in top_villages:
    print(f"  {village}: {count} residents")

# SECTION 2: COUNCIL DATA
print("\n🏛️ COUNCIL STATISTICS")
print("-" * 40)
cursor.execute('SELECT COUNT(*), SUM(allocation) FROM council_pins')
council_count, council_total = cursor.fetchone()
print(f"Council Members: {council_count}")
print(f"Total Fund: R{council_total:,.2f}")
print(f"With Alpha (1.25x): R{council_total * 1.25:,.2f}")

# SECTION 3: MIGRATED COMPONENTS
print("\n📦 MIGRATED COMPONENTS")
print("-" * 40)
cursor.execute('SELECT category, COUNT(*) FROM migrated_components GROUP BY category ORDER BY category')
components = cursor.fetchall()
for category, count in components:
    print(f"  {category}: {count} components")

# SECTION 4: ORCHESTRATOR INTELLIGENCE
print("\n🧠 ORCHESTRATOR INTELLIGENCE")
print("-" * 40)
try:
    from migrated.priority1_core import master_orchestrator
    print("  ✅ Master Orchestrator active")
except:
    print("  ⚠️ Master Orchestrator not loaded")

# Try to read from migrated data
vault_db = Path("migrated/data/vault.db")
if vault_db.exists():
    v_conn = get_db_connection()
    v_cursor = v_conn.cursor()
    v_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = v_cursor.fetchall()
    print(f"  🗄️ Vault DB: {len(tables)} tables")
    v_conn.close()

# SECTION 5: GAUTENG STATUS
print("\n🏭 GAUTENG INDUSTRIAL STATUS")
print("-" * 40)
gauteng_json = Path("migrated/configs/gauteng_nodes.json")
if gauteng_json.exists():
    with open(gauteng_json) as f:
        gauteng = json.load(f)
    total_current = 0
    total_target = 0
    for node in gauteng:
        total_current += node.get('current', 0)
        total_target += node.get('target', 0)
    print(f"  Grid Power: R{total_current:,.2f} / R{total_target:,.2f} ({total_current/total_target*100:.1f}%)")

# SECTION 6: BACKUP STATUS
print("\n🗄️ BACKUP STATUS")
print("-" * 40)
backup_dir = Path.home() / "imperial_vault/archives"
if backup_dir.exists():
    backups = [f for f in backup_dir.glob("*.tar.gz") if os.path.exists(f"{f}.sha256")]
    print(f"  Eternal Backups: {len(backups)}")
    if backups:
        latest = max(backups, key=lambda p: p.stat().st_mtime)
        print(f"  Latest: {latest.name}")

# SECTION 7: SOVEREIGN INFO
print("\n👑 SOVEREIGN INFORMATION")
print("-" * 40)
cursor.execute("SELECT id, username, phone, village, created_at FROM user WHERE username='humbulani_mudau'")
sovereign = cursor.fetchone()
if sovereign:
    print(f"  ID: {sovereign[0]}")
    print(f"  Username: {sovereign[1]}")
    print(f"  Phone: {sovereign[2]}")
    print(f"  Village: {sovereign[3]}")
    print(f"  Since: {sovereign[4][:10]}")

conn.close()

print("\n" + "=" * 70)
print("🏛️ IMPERIAL NETWORK - FULLY OPERATIONAL")
print("=" * 70)
