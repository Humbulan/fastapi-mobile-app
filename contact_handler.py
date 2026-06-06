#!/usr/bin/env python3
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

LOG_FILE = '/data/data/com.termux/files/home/imperial_network/contacts.json'

class ContactHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        if self.path == '/submit':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
                # Add received timestamp
                data['received'] = datetime.now().isoformat()
                # Append to log file
                if os.path.exists(LOG_FILE):
                    with open(LOG_FILE, 'r') as f:
                        try:
                            logs = json.load(f)
                        except:
                            logs = []
                else:
                    logs = []
                logs.append(data)
                with open(LOG_FILE, 'w') as f:
                    json.dump(logs, f, indent=2)
                # Print to terminal (so you see it in the console)
                print(f"\n📨 New contact message from {data.get('name')} ({data.get('email')})")
                print(f"   Project: {data.get('projectType')}")
                print(f"   Message: {data.get('message')[:100]}...\n")
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'ok'}).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress default logging
        pass

if __name__ == '__main__':
    port = 8109
    server = HTTPServer(('0.0.0.0', port), ContactHandler)
    print(f"Contact handler listening on port {port}")
    server.serve_forever()
