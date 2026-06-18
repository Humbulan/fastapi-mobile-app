#!/usr/bin/env python3
from db_config import get_db_connection
"""
🔄 SADC-TO-VILLAGE SYNC TRIGGER
Updates village ranks when large SADC Logistics payments clear
"""
import sqlite3
import random
from datetime import datetime

print("🔄 SADC-TO-VILLAGE SYNC TRIGGER")
print("="*60)

conn = get_db_connection()
cursor = conn.cursor()

# 1. Find recent SADC_A_LOGISTICS payments over R100k
cursor.execute('''
    SELECT payment_id, amount, created_at 
    FROM payment 
    WHERE payment_method='SADC_A_LOGISTICS' 
    AND amount > 100000
    AND status='pending'
    ORDER BY created_at DESC
    LIMIT 10
''')
large_payments = cursor.fetchall()

print(f"\n📦 Found {len(large_payments)} large SADC payments (>R100k)")

# 2. Get current village rankings
cursor.execute('''
    SELECT village, items, rank 
    FROM village_performance 
    ORDER BY items DESC
''')
villages = cursor.fetchall()

print("\n🏘️ CURRENT VILLAGE RANKINGS:")
for village, items, rank in villages[:5]:
    print(f"  {rank}. {village}: {items} items")

# 3. Trigger sync for each payment
triggered = 0
for payment in large_payments:
    payment_id, amount, timestamp = payment
    
    # Select a random top village to reward
    target_village = random.choice([v[0] for v in villages[:5]])
    
    # Update village items
    cursor.execute('''
        UPDATE village_performance 
        SET items = items + 1 
        WHERE village = ?
    ''', (target_village,))
    
    # Mark payment as synced
    cursor.execute('''
        UPDATE payment 
        SET status = 'synced' 
        WHERE payment_id = ?
    ''', (payment_id,))
    
    triggered += 1
    print(f"\n✅ TRIGGERED: Payment R{amount:,.2f} → {target_village} +1 item")

conn.commit()

# 4. Show updated rankings
cursor.execute('''
    SELECT village, items, rank 
    FROM village_performance 
    ORDER BY items DESC
''')
updated = cursor.fetchall()

print("\n📊 UPDATED VILLAGE RANKINGS:")
for village, items, rank in updated[:5]:
    change = "+1" if village in [v[0] for v in villages[:5]] else ""
    print(f"  {rank}. {village}: {items} items {change}")

# 5. Log the sync event
cursor.execute('''
    INSERT INTO imperial_metrics (metric_name, metric_value, metric_text, recorded_at)
    VALUES (?, ?, ?, ?)
''', ('village_sync', len(large_payments), f'Synced {triggered} payments at {datetime.now()}', datetime.now().isoformat()))

conn.commit()
conn.close()

print(f"\n✅ Sync complete: {triggered} village items added")
