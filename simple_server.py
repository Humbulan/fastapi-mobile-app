#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 8089  # Free port (not in dawn report)

os.chdir(os.path.expanduser('~/imperial_network'))

handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), handler) as httpd:
    print(f"\n🏛️ IMPERIAL OMEGA DASHBOARD")
    print(f"================================")
    print(f"🌐 http://localhost:{PORT}")
    print(f"================================")
    print(f"✅ Serving Imperial_standalone.html")
    print(f"================================")
    httpd.serve_forever()
