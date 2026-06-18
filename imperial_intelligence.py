#!/usr/bin/env python3
from db_config import get_db_connection
"""
Imperial Intelligence Dashboard - Master Orchestrator Data
"""
import sqlite3
from datetime import datetime

print("🏛️ IMPERIAL INTELLIGENCE DASHBOARD")
print("=" * 60)
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

conn = get_db_connection()
cursor = conn.cursor()

# Imperial Metrics
print("📊 IMPERIAL METRICS:")
cursor.execute('SELECT metric_name, metric_value, metric_text FROM imperial_metrics ORDER BY metric_name')
metrics = cursor.fetchall()
for name, value, text in metrics:
    if name == 'avg_daily_momentum':
        print(f"   📈 Daily Momentum: R{value:,.2f}")
    elif name == 'month_end_prediction':
        print(f"   🔮 Month-end: R{value:,.2f}")
    elif name == 'gauteng_readiness':
        print(f"   🚀 Gauteng Readiness: {value}%")
    elif name == 'power_grid_current':
        print(f"   ⚡ Power Grid: R{value:,.2f} {text if text else ''}")
    else:
        print(f"   {name}: {value}")

# Village Rankings
print("\n🏘️ VILLAGE PERFORMANCE RANKINGS:")
cursor.execute('''
    SELECT rank, village, items FROM village_performance 
    ORDER BY rank LIMIT 10
''')
villages = cursor.fetchall()
for rank, village, items in villages:
    bar = "▓" * int((items/452)*10) + "░" * (10 - int((items/452)*10))
    print(f"   {rank:2d}. {village:15} {items:4d} items {bar}")

# Gauteng Nodes
print("\n🏭 GAUTENG INDUSTRIAL NODES:")
cursor.execute('''
    SELECT node_name, current, target, progress, weekly_growth, node_type 
    FROM gauteng_nodes
''')
nodes = cursor.fetchall()
for node_name, current, target, progress, growth, node_type in nodes:
    bar = "▓" * int(progress/10) + "░" * (10 - int(progress/10))
    print(f"\n   {node_name}")
    print(f"   Type: {node_type}")
    print(f"   R{current:>12,.2f} / R{target:<12,.2f} [{bar}] {progress:.1f}%")
    print(f"   Weekly Growth: R{growth:,.2f}")

# Summary
print("\n" + "=" * 60)
cursor.execute('SELECT SUM(current), SUM(target) FROM gauteng_nodes')
total_current, total_target = cursor.fetchone()
print(f"🏛️ TOTAL GAUTENG POWER: R{total_current:,.2f} / R{total_target:,.2f} ({total_current/total_target*100:.1f}%)")

cursor.execute('SELECT SUM(items) FROM village_performance')
total_items = cursor.fetchone()[0]
print(f"📦 TOTAL VILLAGE ITEMS: {total_items}")

conn.close()
print("=" * 60)
