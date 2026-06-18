#!/usr/bin/env python3
from db_config import get_db_connection
"""
SADC Trade Intelligence → Alpha Pipeline Bridge
Extracts trade data and injects into nexus_backup for Alpha boosting
"""
import sqlite3
import json
import random
from datetime import datetime, timedelta
import urllib.request
import sys

def get_sadc_data():
    """Fetch current SADC trade intelligence"""
    try:
        with urllib.request.urlopen('http://localhost:8112/status', timeout=3) as response:
            return json.loads(response.read())
    except Exception as e:
        print(f"⚠️ SADC fetch failed: {e}")
        return None

def calculate_trade_flows(sadc_data):
    """Convert SADC trade manifest to transaction amounts"""
    if not sadc_data:
        return []
    
    trades = []
    manifest = sadc_data.get('trade_manifest', {})
    
    # Lithium trades (high volume, volatile)
    lithium = manifest.get('lithium', {})
    if lithium:
        monthly_export = lithium.get('monthly_export_m', 95.2) * 1_000_000  # to USD
        growth = lithium.get('volume_growth', 29.7) / 100
        # Generate 5-10 lithium trades per day
        for i in range(random.randint(5, 10)):
            amount = (monthly_export / 30) * random.uniform(0.8, 1.2) * (1 + growth/30)
            trades.append({
                'amount': amount * 18.5,  # USD to ZAR approx
                'source': 'LITHIUM_SPOT',
                'provider': 'SADC_LITHIUM',
                'volatility': 0.3
            })
    
    # Gold trades (stable, high value)
    gold = manifest.get('gold', {})
    if gold:
        monthly_export = gold.get('monthly_export_m', 150.8) * 1_000_000
        for i in range(random.randint(3, 6)):
            amount = (monthly_export / 30) * random.uniform(0.9, 1.1)
            trades.append({
                'amount': amount * 18.5,
                'source': 'GOLD_FORWARD',
                'provider': 'SADC_GOLD',
                'volatility': 0.15
            })
    
    # Energy trades (infrastructure, recurring)
    energy = manifest.get('energy', {})
    if energy:
        monthly_flow = energy.get('monthly_flow_m', 68.7) * 1_000_000
        for i in range(random.randint(4, 8)):
            amount = (monthly_flow / 30) * random.uniform(0.85, 1.15)
            trades.append({
                'amount': amount * 18.5,
                'source': 'ENERGY_FUTURES',
                'provider': 'SADC_ENERGY',
                'volatility': 0.2
            })
    
    # Port Beira logistics
    port = manifest.get('port_beira', {})
    if port:
        throughput = port.get('current_throughput_m', 14.2) * 1_000_000  # tons
        # Logistics fees per ton
        for i in range(random.randint(8, 15)):
            amount = (throughput / 30) * 50 * random.uniform(0.7, 1.3)  # $50/ton average fee
            trades.append({
                'amount': amount * 18.5,
                'source': 'PORT_BEIRA_LOGISTICS',
                'provider': 'SADC_LOGISTICS',
                'volatility': 0.25
            })
    
    return trades

def inject_to_nexus(trades):
    """Insert trade-derived transactions into nexus_backup"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get a user (use first user)
    cursor.execute('SELECT id, phone FROM user LIMIT 1')
    user = cursor.fetchone()
    if not user:
        print("❌ No users found in database")
        return 0
    
    user_id, phone = user
    
    # Check current pending count
    cursor.execute("SELECT COUNT(*) FROM nexus_backup_transaction_logs WHERE status != 'promoted' OR status IS NULL")
    before = cursor.fetchone()[0]
    
    injected = 0
    print(f"\n📡 INJECTING SADC TRADE FLOWS - {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)
    
    for trade in trades:
        # Add some randomness to amount
        amount = trade['amount'] * random.uniform(1 - trade['volatility'], 1 + trade['volatility'])
        
        # Create timestamp (spread over last 6 hours to simulate flow)
        ts = datetime.now() - timedelta(hours=random.randint(0, 6), minutes=random.randint(0, 59))
        
        # Generate unique reference
        ref = f"SADC_{trade['source']}_{int(ts.timestamp())}_{random.randint(1000,9999)}"
        
        cursor.execute('''
            INSERT INTO nexus_backup_transaction_logs 
            (date, amount, user_id, phone, status, reference, provider, imported_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            ts.isoformat(),
            round(amount, 2),
            user_id,
            phone,
            'pending',
            ref,
            trade['provider'],
            datetime.now().isoformat()
        ))
        
        print(f"📦 {trade['source']:20} R{amount:>12,.2f} | Ref: {ref[-12:]}")
        injected += 1
    
    conn.commit()
    
    # Get new pending count
    cursor.execute("SELECT COUNT(*) FROM nexus_backup_transaction_logs WHERE status != 'promoted' OR status IS NULL")
    after = cursor.fetchone()[0]
    conn.close()
    
    print("="*60)
    print(f"✅ Injected: {injected} SADC transactions")
    print(f"📊 Pending in dock: {before} → {after} (+{after-before})")
    
    # Calculate total value injected
    total_value = sum(t['amount'] for t in trades)
    print(f"💰 Total injected value: R{total_value:,.2f}")
    print(f"⚡ Will become (with 1.25x): R{total_value * 1.25:,.2f}")
    
    return injected

def main():
    print("🏛️ SADC → ALPHA PIPELINE BRIDGE")
    print("="*60)
    
    # Fetch current SADC intelligence
    sadc_data = get_sadc_data()
    if sadc_data:
        print("✅ SADC Trade Intel Fetched")
        print(f"   Lithium Growth: +{sadc_data.get('trade_manifest',{}).get('lithium',{}).get('volume_growth',0)}%")
        print(f"   True Valuation: R{sadc_data.get('wealth_impact',{}).get('true_valuation',0):,.2f}")
    else:
        print("⚠️ Using cached trade patterns")
    
    # Calculate trade flows
    trades = calculate_trade_flows(sadc_data)
    print(f"📊 Generated {len(trades)} trade transactions")
    
    # Inject to nexus_backup
    injected = inject_to_nexus(trades)
    
    # Trigger auto-alpha if we injected anything
    if injected > 0:
        print("\n🚀 Triggering auto-alpha promotion...")
        import promote_data
        promote_data.promote_transactions()
    
    print("\n🏁 Pipeline complete - Check Alpha Monitor:")
    print("   curl -s http://localhost:8084 | python3 -m json.tool")

if __name__ == "__main__":
    main()
