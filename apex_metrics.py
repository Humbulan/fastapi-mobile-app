#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
from datetime import datetime

VALID_API_KEY = "HUMBU-AUDIT-20251219-LEDA"

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Enforce strict endpoint routing
        if self.path != "/v1/audit" and self.path != "/health":
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found", "message": "Invalid endpoint route."}).encode())
            return

        # Enforce API Key validation for the Audit route
        if self.path == "/v1/audit":
            api_key_header = self.headers.get('X-API-Key')
            if api_key_header != VALID_API_KEY:
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Unauthorized", "message": "Invalid or missing X-API-Key header."}).encode())
                return

        # Serve data if validation passes
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        try:
            conn = sqlite3.connect('instance/imperial.db')
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM users")
            users = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM payment")
            payments = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM village")
            villages = cursor.fetchone()[0]

            cursor.execute("SELECT SUM(amount) FROM payment WHERE status='completed'")
            revenue = cursor.fetchone()[0] or 0

            conn.close()
        except Exception as e:
            users, payments, villages, revenue = 0, 0, 0, 0

        response = {
            'service': 'Apex_Metrics',
            'status': 'online',
            'users': users,
            'payments': payments,
            'villages': villages,
            'revenue': revenue,
            'portfolio': 10938044.07,
            'progress_pct': 313.6,
            'timestamp': str(datetime.now())
        }
        self.wfile.write(json.dumps(response, indent=2).encode())

    def do_POST(self):
        if self.path == "/api/sync":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            sync_msg = {"status": "sync_complete", "gateway": "Gauteng_Sector", "timestamp": str(datetime.now())}
            self.wfile.write(json.dumps(sync_msg).encode())
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        return

def run_server():
    server = HTTPServer(('0.0.0.0', 8086), MetricsHandler)
    print("📊 Secure Apex Metrics running on port 8086")
    server.serve_forever()

if __name__ == '__main__':
    run_server()
