#!/usr/bin/env python3
from db_config import get_db_connection
"""
🔄 SADC-TO-VILLAGE SYNC - SCALED VERSION
Rewards all 40 villages based on SADC logistics payments
"""
import sqlite3
import random
from datetime import datetime

print("🔄 SADC-TO-VILLAGE SYNC - SCALED (40 VILLAGES)")
print("="*60)

conn = get_db_connection()
cursor = conn.cursor()

# 1. Get all villages from users table
cursor.execute('''
    SELECT DISTINCT village, COUNT(*) as population
    FROM users
    WHERE village IS NOT NULL AND village != ''
    GROUP BY village
    ORDER BY population DESC
''')
all_villages = cursor.fetchall()

print(f"\n🏘️ FOUND {len(all_villages)} VILLAGES IN SYSTEM")

# 2. Find recent SADC_A_LOGISTICS payments over R50k
cursor.execute('''
    SELECT payment_id, amount, created_at 
    FROM payment 
    WHERE payment_method='SADC_A_LOGISTICS' 
    AND amount > 50000
    AND status='pending'
    ORDER BY created_at DESC
''')
large_payments = cursor.fetchall()

print(f"\n📦 Found {len(large_payments)} large SADC payments (>R50k)")

# 3. Distribute payments across ALL villages
triggered = 0
village_rewards = {}

for payment in large_payments:
    payment_id, amount, timestamp = payment
    
    # Select a random village (weighted by population)
    villages_list = [v[0] for v in all_villages]
    weights = [v[1] for v in all_villages]  # population weight
    
    target_village = random.choices(villages_list, weights=weights, k=1)[0]
    
    # Track rewards per village
    village_rewards[target_village] = village_rewards.get(target_village, 0) + 1
    
    # Update village items in village_performance (create if not exists)
    cursor.execute('''
        INSERT INTO village_performance (village, items, rank, recorded_at)
        VALUES (?, 1, (SELECT COUNT(*)+1 FROM village_performance), ?)
        ON CONFLICT(village) DO UPDATE SET items = items + 1
    ''', (target_village, datetime.now().isoformat()))
    
    # Mark payment as synced
    cursor.execute('''
        UPDATE payment 
        SET status = 'synced' 
        WHERE payment_id = ?
    ''', (payment_id,))
    
    triggered += 1
    print(f"  ✅ R{amount:,.2f} → {target_village} +1 item")

conn.commit()

# 4. Show distribution
print(f"\n📊 REWARD DISTRIBUTION:")
for village, count in sorted(village_rewards.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  • {village}: +{count} items")

# 5. Get updated top 10
cursor.execute('''
    SELECT village, items 
    FROM village_performance 
    ORDER BY items DESC 
    LIMIT 10
''')
top10 = cursor.fetchall()

print(f"\n🏆 TOP 10 VILLAGES NOW:")
for village, items in top10:
    change = "↑" if village in village_rewards else "="
    print(f"  {change} {village}: {items} items")

conn.close()
print(f"\n✅ Scaled sync complete: {triggered} villages rewarded")
