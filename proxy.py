#!/usr/bin/env python3
import http.server
import socketserver
import urllib.request
import os

API_BASE = "http://localhost:8089"

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/challenges'):
            self._proxy('GET', '/challenges')
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith('/submit'):
            self._proxy('POST', '/submit')
        else:
            self.send_response(404)
            self.end_headers()

    def _proxy(self, method, path):
        try:
            body = None
            if method == 'POST':
                length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(length)

            req = urllib.request.Request(API_BASE + path, data=body, method=method)
            if self.headers.get('Content-Type'):
                req.add_header('Content-Type', self.headers['Content-Type'])

            with urllib.request.urlopen(req) as resp:
                self.send_response(resp.status)
                self.send_header('Content-Type', resp.headers.get('Content-Type', 'application/json'))
                self.end_headers()
                self.wfile.write(resp.read())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

PORT = 8084
with socketserver.TCPServer(("0.0.0.0", PORT), ProxyHandler) as httpd:
    print(f"✅ CTF Portal running at http://localhost:{PORT}")
    httpd.serve_forever()
