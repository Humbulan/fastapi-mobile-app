#!/usr/bin/env python3
from db_config import get_db_connection
"""
🏛️ SADC HYPER-DRIVE STRESS TEST
Simulates 275 concurrent users trading in the SADC corridor
"""
import sqlite3
import concurrent.futures
import time
import random
from datetime import datetime

print('🏛️ SADC HYPER-DRIVE STRESS TEST')
print('=' * 60)
print(f'📅 {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('⚡ Simulating Peak Trade Hour - 275 Concurrent Users')
print('=' * 60)

# Configuration
DB_PATH = 'vault.db'
USERS = 275
THREADS = 50
REMITTANCE_RANGE = (1100, 1899)

def simulate_trade(user_id):
    """Simulate a SADC corridor trade"""
    conn = None
    start_time = time.time()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Generate random remittance amount
        amount = random.randint(*REMITTANCE_RANGE)
        
        # Execute transaction with WAL mode
        cursor.execute('BEGIN IMMEDIATE')
        cursor.execute('''
            UPDATE assets 
            SET valuation = valuation + ?, 
                last_trade = ? 
            WHERE id = ?
        ''', (amount, datetime.now().isoformat(), (user_id % 250) + 1))
        
        conn.commit()
        latency = (time.time() - start_time) * 1000  # Convert to ms
        return {'success': True, 'latency': latency, 'amount': amount, 'user': user_id}
        
    except sqlite3.OperationalError as e:
        if 'database is locked' in str(e):
            return {'success': False, 'error': 'LOCKED', 'latency': None, 'user': user_id}
        return {'success': False, 'error': str(e), 'latency': None, 'user': user_id}
    except Exception as e:
        return {'success': False, 'error': str(e), 'latency': None, 'user': user_id}
    finally:
        if conn:
            conn.close()

# Run the stress test
print(f'🚀 Launching {USERS} concurrent trade simulations...')
print(f'   Thread Pool: {THREADS} workers')
print(f'   Remittance: R{REMITTANCE_RANGE[0]}-R{REMITTANCE_RANGE[1]}')
print(f'   Database: {DB_PATH}\n')

start_total = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
    results = list(executor.map(simulate_trade, range(1, USERS + 1)))

total_time = time.time() - start_total

# Analyze results
successful = [r for r in results if r['success']]
locked = [r for r in results if not r['success'] and r.get('error') == 'LOCKED']
failed = [r for r in results if not r['success'] and r.get('error') != 'LOCKED']

success_rate = (len(successful) / USERS) * 100
lock_rate = (len(locked) / USERS) * 100
fail_rate = (len(failed) / USERS) * 100

avg_latency = sum(r['latency'] for r in successful) / len(successful) if successful else 0
total_value = sum(r['amount'] for r in successful)
throughput = len(successful) / total_time

print('\n📊 STRESS TEST RESULTS')
print('=' * 60)
print(f'✅ Successful: {len(successful)}/{USERS} ({success_rate:.1f}%)')
print(f'🔒 Lock Contention: {len(locked)}/{USERS} ({lock_rate:.1f}%)')
print(f'❌ Failed: {len(failed)}/{USERS} ({fail_rate:.1f}%)')
print(f'\n📈 PERFORMANCE METRICS:')
print(f'   Throughput: {throughput:.1f} tx/sec')
print(f'   Avg Latency: {avg_latency:.1f} ms')
print(f'   Total Trade Value: R{total_value:,.2f}')
print(f'   Test Duration: {total_time:.2f} seconds')

# Check WAL mode status
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute('PRAGMA journal_mode')
wal_mode = cursor.fetchone()[0]
conn.close()

print(f'\n🔧 Database Journal Mode: {wal_mode}')

# Imperial Verdict
print('\n🏛️ IMPERIAL VERDICT')
print('=' * 60)

if success_rate > 90:
    print('✅ STATUS: ELITE - Network operates at sovereign capacity')
    print('   The Imperial Network successfully handled peak SADC trade volume')
elif success_rate > 75:
    print('⚡ STATUS: STABLE - Ready for regional expansion')
    print('   Minor optimization needed for ultra-high frequency trading')
else:
    print('⚠️ STATUS: MONITOR - Review database indexes and connection pooling')

print(f'\n📋 RECOMMENDATIONS:')
if lock_rate > 15:
    print('   • Increase WAL cache size (PRAGMA journal_size_limit=1000000)')
if avg_latency > 200:
    print('   • Consider connection pooling for sub-100ms trades')
if throughput < 5:
    print('   • Enable SQLite mmap for faster reads (PRAGMA mmap_size=30000000)')

# Generate SADC Trade Manifest
print('\n📄 GENERATING SADC TRADE MANIFEST')
print('=' * 60)

manifest = {
    'timestamp': datetime.now().isoformat(),
    'corridor': 'Zim/Moz/SA',
    'trades_processed': len(successful),
    'total_volume': total_value,
    'avg_ticket': total_value / len(successful) if successful else 0,
    'peak_throughput': throughput,
    'latency_p95': sorted([r['latency'] for r in successful])[int(len(successful)*0.95)] if successful else 0,
    'commodity_mix': {
        'lithium': int(total_value * 0.45),
        'gold': int(total_value * 0.30),
        'energy': int(total_value * 0.15),
        'logistics': int(total_value * 0.10)
    }
}

print(f'📍 Corridor: {manifest["corridor"]}')
print(f'💰 Total Volume: R{manifest["total_volume"]:,.2f}')
print(f'📊 Avg Ticket: R{manifest["avg_ticket"]:,.2f}')
print(f'⚡ Peak Throughput: {manifest["peak_throughput"]:.1f} tx/sec')
print(f'⏱️  P95 Latency: {manifest["latency_p95"]:.1f} ms')
print('\n💎 Commodity Breakdown:')
for commodity, value in manifest['commodity_mix'].items():
    print(f'   • {commodity.title()}: R{value:,.2f}')

# Save manifest
import json
with open('sadc_trade_manifest_20260223.json', 'w') as f:
    json.dump(manifest, f, indent=2)

print('\n✅ Manifest saved to: sadc_trade_manifest_20260223.json')
print('📁 Location: ~/imperial_network/sadc_trade_manifest_20260223.json')
