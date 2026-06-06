#!/usr/bin/env python3
"""
MoMo Payment Statistics for Imperial Omega
Fixed version - handles string amounts properly
"""

import json
import os
import subprocess
from datetime import datetime, timedelta

def get_momo_transactions():
    """Parse MoMo transactions from log file"""
    log_file = os.path.expanduser('~/imperial_network/logs/momo_transactions.log')
    transactions = []
    
    try:
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    # Ensure amount is float
                    if 'amount' in data:
                        data['amount'] = float(data['amount'])
                    # Add timestamp if not present
                    if 'timestamp' not in data:
                        data['timestamp'] = datetime.now().isoformat()
                    transactions.append(data)
                except Exception as e:
                    print(f"Error parsing line: {e}")
                    pass
    except FileNotFoundError:
        print("No transactions log found yet")
    
    return transactions

def calculate_stats(transactions):
    """Calculate payment statistics"""
    if not transactions:
        return {
            'total_amount': 0,
            'total_transactions': 0,
            'average_amount': 0,
            'unique_payers': 0,
            'last_24h_amount': 0,
            'last_24h_count': 0
        }
    
    # Convert all amounts to float
    amounts = [float(t.get('amount', 0)) for t in transactions]
    total_amount = sum(amounts)
    total_count = len(transactions)
    avg_amount = total_amount / total_count if total_count > 0 else 0
    
    # Get unique payers
    unique_payers = len(set(t.get('payer', {}).get('partyId', '') for t in transactions))
    
    # Last 24 hours
    cutoff = datetime.now() - timedelta(hours=24)
    recent = []
    for t in transactions:
        try:
            ts = datetime.fromisoformat(t.get('timestamp', '2000-01-01'))
            if ts > cutoff:
                recent.append(t)
        except:
            pass
    
    recent_amount = sum(float(t.get('amount', 0)) for t in recent)
    recent_count = len(recent)
    
    return {
        'total_amount': total_amount,
        'total_transactions': total_count,
        'average_amount': avg_amount,
        'unique_payers': unique_payers,
        'last_24h_amount': recent_amount,
        'last_24h_count': recent_count
    }

def generate_momo_report():
    """Generate MoMo payment report"""
    print("📊 Generating MoMo Stats Report...")
    transactions = get_momo_transactions()
    stats = calculate_stats(transactions)
    
    print(f"   Transactions found: {stats['total_transactions']}")
    print(f"   Total amount: R{stats['total_amount']:,.2f}")
    
    # Generate HTML report
    report_path = os.path.expanduser('~/humbu_community_nexus/momo_report.html')
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Imperial Omega - MoMo Payment Report</title>
    <style>
        body {{ background: linear-gradient(135deg, #0a0a0f 0%, #0f0f1a 100%); color: #00ff00; font-family: monospace; padding: 40px; }}
        .container {{ max-width: 900px; margin: 0 auto; background: rgba(26, 26, 46, 0.95); border: 1px solid #00ff00; padding: 30px; border-radius: 12px; box-shadow: 0 0 20px rgba(0, 255, 0, 0.1); }}
        h1 {{ color: #ffd700; text-align: center; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }}
        .stat {{ background: #0f0f1a; padding: 20px; border-left: 4px solid #00ff00; border-radius: 8px; transition: transform 0.3s; }}
        .stat:hover {{ transform: translateY(-5px); }}
        .value {{ font-size: 32px; font-weight: bold; color: #ffd700; }}
        .label {{ color: #888; font-size: 12px; margin-top: 10px; }}
        .transactions {{ margin-top: 30px; max-height: 400px; overflow-y: auto; }}
        .tx {{ background: #0a0a0f; padding: 10px; margin: 5px 0; border-left: 2px solid #00ff00; font-size: 12px; }}
        .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #00ff00; font-size: 0.8em; color: #888; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📱 Imperial Omega - MoMo Payment Gateway</h1>
        <p style="text-align: center;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S SAST')}</p>
        
        <div class="stats-grid">
            <div class="stat">
                <div class="value">R{stats['total_amount']:,.2f}</div>
                <div class="label">Total Revenue (MoMo)</div>
            </div>
            
            <div class="stat">
                <div class="value">{stats['total_transactions']}</div>
                <div class="label">Total Transactions</div>
            </div>
            
            <div class="stat">
                <div class="value">R{stats['average_amount']:,.2f}</div>
                <div class="label">Average Transaction</div>
            </div>
            
            <div class="stat">
                <div class="value">{stats['unique_payers']}</div>
                <div class="label">Unique Payers</div>
            </div>
            
            <div class="stat">
                <div class="value">R{stats['last_24h_amount']:,.2f}</div>
                <div class="label">Last 24 Hours</div>
            </div>
            
            <div class="stat">
                <div class="value">{stats['last_24h_count']}</div>
                <div class="label">Last 24h Transactions</div>
            </div>
        </div>
        
        <h3>📋 Recent Transactions</h3>
        <div class="transactions">
            {''.join([f'<div class="tx">💰 R{float(t.get("amount", 0)):.2f} | 📱 {t.get("payer", {}).get("partyId", "Unknown")} | 🕐 {t.get("timestamp", "Unknown")[:19]}</div>' for t in transactions[:20]])}
        </div>
        
        <div class="footer">
            🏛️ Imperial Omega Sovereign Payment System | Callback Endpoint: /momo/callback<br>
            Status: ACTIVE | Tracking: {stats['total_transactions']} transactions
        </div>
    </div>
</body>
</html>
    """
    
    with open(report_path, 'w') as f:
        f.write(html)
    
    print(f"✅ MoMo report generated: {report_path}")
    return stats

if __name__ == '__main__':
    generate_momo_report()
