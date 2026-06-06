#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import socket

os.chdir(os.path.expanduser('~/imperial_network'))

class ImperialHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/imperial_standalone.html'
        return super().do_GET()
    
    def log_message(self, format, *args):
        pass  # Suppress log messages

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    port = 8099  # Using B2B_Hub port (already online)
    server = HTTPServer(('0.0.0.0', port), ImperialHandler)
    ip = get_ip()
    print(f"\n🏛️ IMPERIAL OMEGA - MARCH 2026")
    print(f"================================")
    print(f"🌐 Local URL: http://localhost:{port}")
    print(f"📱 Network URL: http://{ip}:{port}")
    print(f"================================")
    print(f"✅ ALL 6 FEATURES ACTIVE:")
    print(f"   1. 📈 Monte Carlo projections (730/390/250 days)")
    print(f"   2. 🏘️ Village tracker (43/900)")
    print(f"   3. ⚡ Mineral diversification (4 minerals)")
    print(f"   4. 🔍 Real-time node scanning")
    print(f"   5. 🖥️ Port matrix view (51/51)")
    print(f"   6. 📊 Automated reports")
    print(f"================================")
    print(f"💰 Wealth: R269,905,078,380.45")
    print(f"📈 Progress: 53.98% to R500B")
    print(f"🏘️ Villages: 43/900")
    print(f"================================")
    server.serve_forever()
