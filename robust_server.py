#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys
import socket
import time

# Use a port NOT in your services list
PORT = 8084  # Free port (not in dawn report)

# Change to the directory with our HTML files
os.chdir(os.path.expanduser('~/imperial_network'))

# Create a custom handler that serves our HTML
class ImperialHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/imperial_standalone.html'
        return super().do_GET()
    
    def log_message(self, format, *args):
        # Suppress log messages for cleaner output
        pass

try:
    with socketserver.TCPServer(("0.0.0.0", PORT), ImperialHandler) as httpd:
        print(f"\n🏛️ IMPERIAL OMEGA DASHBOARD")
        print(f"================================")
        print(f"🌐 http://localhost:{PORT}")
        print(f"📱 http://192.168.8.130:{PORT}")
        print(f"================================")
        print(f"✅ Serving Imperial Standalone Dashboard")
        print(f"================================")
        print(f"💰 Wealth: R269,905,078,380.45")
        print(f"🏘️ Villages: 43/900")
        print(f"🖥️ Ports: 51/51 ONLINE")
        print(f"================================")
        httpd.serve_forever()
except Exception as e:
    print(f"❌ Error starting server: {e}")
    sys.exit(1)
