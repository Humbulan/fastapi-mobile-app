#!/usr/bin/env python3
from db_config import get_db_connection
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
from datetime import datetime

class IDCHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(amount) FROM payment WHERE payment_method='IMPERIAL_WEB_UPGRADE'")
            total = cursor.fetchone()[0] or 0
            cursor.execute("SELECT COUNT(*) FROM payment WHERE payment_method='IMPERIAL_WEB_UPGRADE'")
            count = cursor.fetchone()[0]
            conn.close()
        except:
            total, count = 0, 0
        
        response = {
            'service': 'IMPERIAL_WEB_UPGRADE',
            'port': 8106,
            'total_capital': total,
            'transactions': count,
            'status': 'online',
            'timestamp': str(datetime.now())
        }
        self.wfile.write(json.dumps(response).encode())

if __name__ == '__main__':
    print(f"💰 IDC Dividend port 8106 (IMPERIAL_WEB_UPGRADE) starting...")
    HTTPServer(('0.0.0.0', 8106), IDCHandler).serve_forever()
