#!/usr/bin/env python3
from db_config import get_db_connection
"""
🏭 IMPERIAL INDUSTRIAL BRIDGE
Connects SADC Logistics revenue to Gauteng manufacturing nodes
"""
import sqlite3
from datetime import datetime

print("🏭 IMPERIAL INDUSTRIAL BRIDGE")
print("="*60)

conn = get_db_connection()
cursor = conn.cursor()

# 1. Get current Gauteng node status
cursor.execute('''
    SELECT node_name, current, target, progress 
    FROM gauteng_nodes 
    ORDER BY node_name
''')
nodes = cursor.fetchall()

print("\n📊 CURRENT GAUTENG STATUS:")
for node, current, target, progress in nodes:
    needed = target - current
    print(f"  {node:25} | R{current:>10,.2f} / R{target:<10,.2f} | {progress:5.1f}% | Need: R{needed:>10,.2f}")

# 2. Get SADC_A_LOGISTICS available capital
cursor.execute('''
    SELECT SUM(amount) FROM payment 
    WHERE payment_method='SADC_A_LOGISTICS' AND status='pending'
''')
sadc_a = cursor.fetchone()[0] or 0

print(f"\n🚚 SADC_A_LOGISTICS AVAILABLE: R{sadc_a:,.2f}")

# 3. Calculate allocation
total_needed = 0
allocation_plan = []

for node, current, target, progress in nodes:
    needed = target - current
    if needed > 0:
        total_needed += needed
        allocation_plan.append((node, needed))

# 4. Strategic allocation (2.6% of SADC_A covers all needs)
allocation_pct = (total_needed / sadc_a) * 100 if sadc_a > 0 else 0

print(f"\n📈 BRIDGE ANALYSIS:")
print(f"  Total capital needed: R{total_needed:,.2f}")
print(f"  SADC_A allocation required: {allocation_pct:.2f}% (R{total_needed:,.2f})")

# 5. Execute allocation
if sadc_a >= total_needed:
    print(f"\n🚀 EXECUTING INDUSTRIAL BRIDGE:")
    
    # Update Gauteng nodes
    for node, needed in allocation_plan:
        cursor.execute('''
            UPDATE gauteng_nodes 
            SET current = current + ?,
                progress = ((current + ?) / target) * 100
            WHERE node_name = ?
        ''', (needed, needed, node))
        print(f"  ✅ {node}: +R{needed:,.2f}")
    
    # Mark SADC_A as allocated (optional - move to completed)
    cursor.execute('''
        UPDATE payment 
        SET status = 'bridged' 
        WHERE payment_method='SADC_A_LOGISTICS' 
        AND status='pending'
        LIMIT ?
    ''', (len(allocation_plan),))
    
    conn.commit()
    
    # Show updated status
    print(f"\n📊 UPDATED GAUTENG STATUS:")
    cursor.execute('''
        SELECT node_name, current, target, progress 
        FROM gauteng_nodes 
        ORDER BY node_name
    ''')
    for node, current, target, progress in cursor.fetchall():
        print(f"  {node:25} | R{current:>10,.2f} / R{target:<10,.2f} | {progress:5.1f}%")
    
else:
    print(f"\n⚠️  Insufficient SADC_A capital. Need R{total_needed - sadc_a:,.2f} more.")

# 6. Create bridge record
cursor.execute('''
    INSERT INTO payment (payment_id, amount, payment_method, status, created_at)
    VALUES (?, ?, ?, 'bridged', ?)
''', (f"BRIDGE_{datetime.now().strftime('%Y%m%d_%H%M%S')}", total_needed, 'INDUSTRIAL_BRIDGE', datetime.now().isoformat()))

conn.commit()
conn.close()

print(f"\n✅ Industrial Bridge complete at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
