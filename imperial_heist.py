#!/usr/bin/env python3
from db_config import get_db_connection
"""
IMPERIAL HEIST - Migrate all valuable assets from old project
"""
import os
import shutil
import sqlite3
from pathlib import Path
from datetime import datetime

OLD_PROJECT = Path.home() / "humbu_community_nexus"
NEW_PROJECT = Path.home() / "imperial_network"

print("🏛️ IMPERIAL HEIST - ASSET MIGRATION")
print("=" * 60)

# Create migration directories
migration_dirs = [
    "migrated/priority1_core",
    "migrated/priority2_financial",
    "migrated/priority3_village",
    "migrated/priority4_gauteng",
    "migrated/priority5_utilities",
    "migrated/data",
    "migrated/configs"
]

for dir_path in migration_dirs:
    (NEW_PROJECT / dir_path).mkdir(parents=True, exist_ok=True)

# Priority 1 - Core Infrastructure
print("\n📦 MIGRATING PRIORITY 1 - CORE INFRASTRUCTURE")
core_files = [
    "master_orchestrator.py",
    "revenue_bridge.py",
    "revenue_engine_8086.py",
    "ussd_interface.py",
    "ussd_transaction_engine.py",
    "government_api.py",
    "health_api.py",
    "imperial_sage.py",
    "imperial_status.py"
]

for file in core_files:
    src = OLD_PROJECT / file
    dst = NEW_PROJECT / "migrated/priority1_core" / file
    if src.exists():
        shutil.copy2(src, dst)
        print(f"   ✅ {file}")
    else:
        print(f"   ⚠️  {file} not found")

# Priority 2 - Financial Systems
print("\n💰 MIGRATING PRIORITY 2 - FINANCIAL SYSTEMS")
financial_files = [
    "transaction_engine_secure.py",
    "merchant_payouts.py",
    "weekly_payout.py",
    "mobile_money_integration.py",
    "cac_reduction.py",
    "cac_reduction_fixed.py",
    "cac_reduction_protocol.py",
    "financial_reality_adjusted.py"
]

for file in financial_files:
    src = OLD_PROJECT / file
    dst = NEW_PROJECT / "migrated/priority2_financial" / file
    if src.exists():
        shutil.copy2(src, dst)
        print(f"   ✅ {file}")
    else:
        print(f"   ⚠️  {file} not found")

# Priority 3 - Village Intelligence
print("\n🏘️ MIGRATING PRIORITY 3 - VILLAGE INTELLIGENCE")
village_files = [
    "village_economics_report.py",
    "village_leaderboard.py",
    "village_alert.py",
    "daily_sales_report.py",
    "daily_sales_report_fixed.py",
    "growth_tracker.py",
    "live_sales_tracker.py"
]

for file in village_files:
    src = OLD_PROJECT / file
    dst = NEW_PROJECT / "migrated/priority3_village" / file
    if src.exists():
        shutil.copy2(src, dst)
        print(f"   ✅ {file}")
    else:
        print(f"   ⚠️  {file} not found")

# Priority 4 - Gauteng Operations
print("\n🏭 MIGRATING PRIORITY 4 - GAUTENG OPERATIONS")
gauteng_files = [
    "gauteng_injection.py",
    "gauteng_monitor.py",
    "gauteng_recruitment.py",
    "sandton_alert.py"
]

for file in gauteng_files:
    src = OLD_PROJECT / file
    dst = NEW_PROJECT / "migrated/priority4_gauteng" / file
    if src.exists():
        shutil.copy2(src, dst)
        print(f"   ✅ {file}")
    else:
        print(f"   ⚠️  {file} not found")

# Priority 5 - Utilities
print("\n🔧 MIGRATING PRIORITY 5 - UTILITIES")
utility_files = [
    "system_heartbeat.py",
    "watchdog.py",
    "weekly_backup.py",
    "generate_whatsapp_templates.py",
    "generate_shop_qr_codes.py",
    "create_qr_gallery.py",
    "generate_clean_qrs.py"
]

for file in utility_files:
    src = OLD_PROJECT / file
    dst = NEW_PROJECT / "migrated/priority5_utilities" / file
    if src.exists():
        shutil.copy2(src, dst)
        print(f"   ✅ {file}")
    else:
        print(f"   ⚠️  {file} not found")

# Migrate critical data files
print("\n📊 MIGRATING DATA FILES")
data_files = [
    ("transactions.csv", "data/"),
    ("council_pins_distribution.csv", "data/"),
    ("gauteng_nodes.json", "configs/"),
    ("reality_corrected.json", "configs/"),
    ("flows.json", "configs/")
]

for file, subdir in data_files:
    src = OLD_PROJECT / file
    dst = NEW_PROJECT / "migrated" / subdir / file
    if src.exists():
        shutil.copy2(src, dst)
        print(f"   ✅ {file}")
    else:
        print(f"   ⚠️  {file} not found")

# Migrate databases
print("\n🗄️ MIGRATING DATABASES")
db_files = [
    ("community_nexus.db", "data/"),
    ("vault.db", "data/")
]

for file, subdir in db_files:
    src = OLD_PROJECT / file
    dst = NEW_PROJECT / "migrated" / subdir / file
    if src.exists():
        shutil.copy2(src, dst)
        print(f"   ✅ {file}")
        
        # Export schema and data from SQLite
        if file.endswith('.db'):
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                print(f"      Tables found: {', '.join([t[0] for t in tables[:5]])}" + 
                      (f" and {len(tables)-5} more" if len(tables) > 5 else ""))
                conn.close()
            except:
                print(f"      Could not read schema")
    else:
        print(f"   ⚠️  {file} not found")

# Create migration report
print("\n" + "=" * 60)
print("📋 MIGRATION REPORT")
print("=" * 60)

# Count migrated files
total_files = 0
for priority_dir in migration_dirs[:5]:  # Only count priority dirs
    dir_path = NEW_PROJECT / priority_dir
    if dir_path.exists():
        count = len(list(dir_path.glob("*.py")))
        print(f"   {priority_dir}: {count} files")
        total_files += count

print(f"\n📦 Total Python files migrated: {total_files}")
print(f"📁 Migration location: ~/imperial_network/migrated/")

# Create integration script
print("\n🔧 Creating integration helper...")
with open(NEW_PROJECT / "migrated/integrate_all.py", 'w') as f:
    f.write("""#!/usr/bin/env python3
\"\"\"
Integration Helper - Import migrated components into Imperial Network
\"\"\"
import os
import sys
from pathlib import Path

print("🏛️ INTEGRATING MIGRATED COMPONENTS")
print("=" * 60)

# Add migrated directories to path
migrated_base = Path(__file__).parent
sys.path.insert(0, str(migrated_base))

# Import priority modules
priority_dirs = [
    "priority1_core",
    "priority2_financial", 
    "priority3_village",
    "priority4_gauteng",
    "priority5_utilities"
]

for priority in priority_dirs:
    priority_path = migrated_base / priority
    if priority_path.exists():
        print(f"\\n📦 Loading {priority}...")
        sys.path.insert(0, str(priority_path))
        
        # List available modules
        py_files = list(priority_path.glob("*.py"))
        for py_file in py_files:
            module_name = py_file.stem
            if not module_name.startswith('_'):
                print(f"   ✅ {module_name}")

print("\\n✅ Integration complete. Available modules:")
print("   from migrated.priority1_core import *")
print("   from migrated.priority2_financial import *")
print("   etc.")
""")

print("\n🏁 Migration complete! Run 'python3 migrated/integrate_all.py' to import")
