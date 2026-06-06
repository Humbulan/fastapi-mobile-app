#!/usr/bin/env python3
"""
MoMo Payment Statistics - JSON Output for Node-RED
"""

import json
import os
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
                    if 'amount' in data:
                        data['amount'] = float(data['amount'])
                    if 'timestamp' not in data:
                        data['timestamp'] = datetime.now().isoformat()
                    transactions.append(data)
                except:
                    pass
    except FileNotFoundError:
        pass
    
    return transactions

def calculate_stats():
    """Calculate and return stats as JSON"""
    transactions = get_momo_transactions()
    
    if not transactions:
        return {
            'total_amount': 0,
            'total_transactions': 0,
            'average_amount': 0,
            'unique_payers': 0,
            'last_24h_amount': 0,
            'last_24h_count': 0,
            'transactions': []
        }
    
    amounts = [float(t.get('amount', 0)) for t in transactions]
    total_amount = sum(amounts)
    total_count = len(transactions)
    avg_amount = total_amount / total_count if total_count > 0 else 0
    
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
    
    # Get last 10 transactions for display
    last_10 = []
    for t in transactions[:10]:
        last_10.append({
            'amount': float(t.get('amount', 0)),
            'payer': t.get('payer', {}).get('partyId', 'Unknown'),
            'timestamp': t.get('timestamp', '')[:19],
            'status': t.get('status', 'SUCCESSFUL')
        })
    
    return {
        'total_amount': total_amount,
        'total_transactions': total_count,
        'average_amount': round(avg_amount, 2),
        'unique_payers': unique_payers,
        'last_24h_amount': round(recent_amount, 2),
        'last_24h_count': recent_count,
        'recent_transactions': last_10,
        'status': 'active',
        'timestamp': datetime.now().isoformat()
    }

if __name__ == '__main__':
    stats = calculate_stats()
    print(json.dumps(stats, indent=2))
