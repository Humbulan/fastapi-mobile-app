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
cursor.execute('SELECT role, COUNT(*) FROM user GROUP BY role ORDER BY role')
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
row = cursor.fetchone()
council_count = row[0] or 0
council_total = row[1] or 0
print(f"Council Members: {council_count}")
print(f"Total Fund: R{council_total:,.2f}")
print(f"With Alpha (1.25x): R{council_total * 1.25:,.2f}")

# SECTION 3: MIGRATED COMPONENTS
print("\n📦 MIGRATED COMPONENTS")
print("-" * 40)
try:
    cursor.execute('SELECT category, COUNT(*) FROM migrated_components GROUP BY category ORDER BY category')
    components = cursor.fetchall()
    for category, count in components:
        print(f"  {category}: {count} components")
except:
    # Count files manually
    migrated_dir = Path("migrated")
    if migrated_dir.exists():
        total_files = 0
        categories = {
            "priority1_core": "Core Infrastructure",
            "priority2_financial": "Financial Systems", 
            "priority3_village": "Village Intelligence",
            "priority4_gauteng": "Gauteng Operations",
            "priority5_utilities": "Utilities"
        }
        for dir_name, display_name in categories.items():
            dir_path = migrated_dir / dir_name
            if dir_path.exists():
                count = len(list(dir_path.glob("*.py")))
                print(f"  {display_name}: {count} files")
                total_files += count
        print(f"\n  Total Python files: {total_files}")

# SECTION 4: ORCHESTRATOR INTELLIGENCE
print("\n🧠 ORCHESTRATOR INTELLIGENCE")
print("-" * 40)
orchestrator_path = Path("migrated/priority1_core/master_orchestrator.py")
if orchestrator_path.exists():
    print("  ✅ Master Orchestrator available")
else:
    print("  ⚠️ Master Orchestrator not found")

# Check migrated databases
vault_db = Path("migrated/data/vault.db")
if vault_db.exists():
    size = vault_db.stat().st_size
    print(f"  🗄️ Vault DB: {size:,} bytes")
else:
    print("  ⚠️ Vault DB not found")

community_db = Path("migrated/data/community_nexus.db")
if community_db.exists():
    size = community_db.stat().st_size
    print(f"  🗄️ Community DB: {size:,} bytes")

# SECTION 5: GAUTENG STATUS
print("\n🏭 GAUTENG INDUSTRIAL STATUS")
print("-" * 40)
gauteng_json = Path("migrated/configs/gauteng_nodes.json")
if gauteng_json.exists():
    try:
        with open(gauteng_json) as f:
            content = f.read()
            # Simple parse since structure might vary
            if "SANDTON" in content:
                print("  ✅ Gauteng config present")
                # Extract some basic info
                import re
                sandton_match = re.search(r'SANDTON.*?R\s*([\d,]+\.\d+)', content)
                if sandton_match:
                    sandton_val = float(sandton_match.group(1).replace(',', ''))
                    print(f"  📊 Sandton Tech: R{sandton_val:,.2f}")
    except:
        print("  ⚠️ Could not parse Gauteng config")
else:
    print("  ⚠️ Gauteng config not found")

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
        print(f"  Size: {latest.stat().st_size:,} bytes")
else:
    print("  No backups found")

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
else:
    print("  Sovereign not found in database")

conn.close()

print("\n" + "=" * 70)
print("🏛️ IMPERIAL NETWORK - FULLY OPERATIONAL")
print(f"📊 {total_users} Users | {council_count} Council | {len(backups) if 'backups' in locals() else 0} Backups")
print("=" * 70)
