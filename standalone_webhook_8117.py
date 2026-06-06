#!/usr/bin/env python3
"""
Simple webhook listener for port 8117.
Accepts POST/GET, logs to file, always returns 200.
Uses only standard library (no Flask required).
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import datetime
import json

class WebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default logging
        pass

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Ukuvuselela Webhook Active')
        self.log_to_file('GET', self.path)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "received"}).encode())
        self.log_to_file('POST', self.path, body)

    def log_to_file(self, method, path, body=''):
        log_line = f"{datetime.datetime.now().isoformat()} {method} {path}"
        if body:
            log_line += f" body: {body[:200]}"
        with open('/data/data/com.termux/files/home/imperial_network/logs/ukuvo_webhook.log', 'a') as f:
            f.write(log_line + '\n')

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8117), WebhookHandler)
    print("Webhook listening on port 8117")
    server.serve_forever()
