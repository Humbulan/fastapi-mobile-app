#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', 'http://localhost:1883')
        self.end_headers()
    
    def log_message(self, format, *args):
        return

print("🔄 Node-RED Redirector starting on port 1880 -> 1883")
HTTPServer(('0.0.0.0', 1880), RedirectHandler).serve_forever()
