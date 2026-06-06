#!/usr/bin/env python3
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            result = subprocess.run(['/data/data/com.termux/files/home/bin/imperial-agent', 'health'], capture_output=True, text=True)
            self.wfile.write(result.stdout.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        self.do_GET()

if __name__ == '__main__':
    port = 8119
    print(f"Health webhook listening on port {port}")
    HTTPServer(('0.0.0.0', port), HealthHandler).serve_forever()
