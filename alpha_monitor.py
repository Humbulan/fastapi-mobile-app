#!/usr/bin/env python3
from db_config import get_db_connection
from http.server import HTTPServer, BaseHTTPRequestHandler
import sqlite3
import json
from datetime import datetime, timedelta

class AlphaHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        conn = get_db_connection()
        c = conn.cursor()
        
        # Get overall stats
        c.execute('SELECT SUM(amount), COUNT(*) FROM payment')
        total, count = c.fetchone()
        total = total or 0
        count = count or 0
        
        # Calculate Alpha impact
        raw_total = total / 1.25
        alpha_boost = total - raw_total
        
        # Last 24h
        c.execute('''
            SELECT SUM(amount), COUNT(*) FROM payment 
            WHERE created_at > datetime('now', '-1 day')
        ''')
        day_total, day_count = c.fetchone()
        day_total = day_total or 0
        
        # Pending transactions
        c.execute('SELECT COUNT(*) FROM nexus_backup_transaction_logs WHERE status != "promoted" OR status IS NULL')
        pending = c.fetchone()[0]
        
        # Project to R500M
        target = 500_000_000
        remaining = target - total
        daily_rate = day_total if day_total > 0 else total / 30 if total > 0 else 0
        days_to_target = remaining / daily_rate if daily_rate > 0 else float('inf')
        
        response = {
            'alpha_multiplier': 1.25,
            'timestamp': datetime.now().isoformat(),
            'portfolio': {
                'total': total,
                'raw_base': raw_total,
                'alpha_boost': alpha_boost,
                'transaction_count': count,
                'progress_percent': (total/target)*100
            },
            'last_24h': {
                'volume': day_total,
                'transactions': day_count,
                'daily_rate': daily_rate
            },
            'pipeline': {
                'pending_in_dock': pending,
                'days_to_R500M': days_to_target,
                'months_to_R500M': days_to_target / 30
            },
            'status': 'ALPHA_ACTIVE'
        }
        
        conn.close()
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response, indent=2).encode())

print("🏛️ Alpha Monitor running on port 8084")
HTTPServer(('', 8084), AlphaHandler).serve_forever()
