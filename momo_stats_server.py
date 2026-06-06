#!/usr/bin/env python3
"""
Simple HTTP server for MoMo Stats - Runs on port 5002
"""

import json
import os
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler

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
            'recent_transactions': [],
            'status': 'active',
            'timestamp': datetime.now().isoformat()
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

class StatsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/momo/stats' or self.path == '/stats':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            stats = calculate_stats()
            self.wfile.write(json.dumps(stats, indent=2).encode())
            
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            html = """
            <html>
            <head><title>Imperial Omega MoMo Stats</title></head>
            <body style="background:#0a0a0f; color:#00ff00; font-family:monospace; padding:40px;">
                <h1>📱 Imperial Omega MoMo Stats</h1>
                <p>Stats endpoint: <a href="/momo/stats">/momo/stats</a></p>
                <p>Callback endpoint: <a href="http://localhost:1880/momo/callback">http://localhost:1880/momo/callback</a></p>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0] if args else format}")

def run():
    port = 5002
    server = HTTPServer(('0.0.0.0', port), StatsHandler)
    print(f"📊 MoMo Stats Server running on port {port}")
    print(f"   Stats: http://localhost:{port}/momo/stats")
    print("Press Ctrl+C to stop")
    server.serve_forever()

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print("\n🛑 Stats server stopped")
