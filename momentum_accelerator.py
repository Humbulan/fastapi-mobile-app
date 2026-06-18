#!/usr/bin/env python3
from db_config import get_db_connection
import sqlite3
from datetime import datetime

# Target Configuration
TARGET_GRID = 600000.00
DEADLINE = "2026-06-16" # Youth Day Milestone

conn = get_db_connection()
cursor = conn.cursor()

# Get Current Status
cursor.execute("SELECT metric_value FROM imperial_metrics WHERE metric_name='power_grid_current'")
current_grid = cursor.fetchone()[0]

cursor.execute("SELECT metric_value FROM imperial_metrics WHERE metric_name='avg_daily_momentum'")
current_momentum = cursor.fetchone()[0]

# Math Logic
gap = TARGET_GRID - current_grid
days_left = (datetime.strptime(DEADLINE, "%Y-%m-%d") - datetime.now()).days
req_daily_avg = gap / days_left
acceleration_needed = req_daily_avg - current_momentum

print(f"🚀 MOMENTUM ACCELERATOR: MISSION {DEADLINE}")
print("=" * 60)
print(f"📊 Current Grid:   R{current_grid:,.2f} ({ (current_grid/TARGET_GRID)*100:.1f}%)")
print(f"🎯 Target Grid:    R{TARGET_GRID:,.2f}")
print(f"🕳️  Imperial Gap:   R{gap:,.2f}")
print(f"📅 Days Remaining: {days_left}")
print("-" * 60)
print(f"⚡ Required Daily: R{req_daily_avg:,.2f}")
print(f"📈 Current Speed:  R{current_momentum:,.2f}")
print(f"🔥 Speed Increase: +R{acceleration_needed:,.2f} per day")
print("-" * 60)

# Village Contribution Targets
print("\n🏘️ VILLAGE CONTRIBUTION TARGETS (Proportional):")
cursor.execute("SELECT village, items FROM village_performance ORDER BY items DESC")
villages = cursor.fetchall()
total_items = sum(v[1] for v in villages)

for village, items in villages:
    share = items / total_items
    v_target = req_daily_avg * share
    print(f"   • {village:15} | Daily Target: R{v_target:,.2f}")

conn.close()
