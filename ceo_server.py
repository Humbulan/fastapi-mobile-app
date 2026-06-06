#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
import re
import os
from datetime import datetime

class CEOHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/ceo'
        
        if self.path == '/ceo':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html_path = os.path.expanduser('~/imperial_network/ceo_mobile.html')
            with open(html_path, 'r') as f:
                self.wfile.write(f.read().encode())
        
        elif self.path == '/api/imperial/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Use expanded path
            script_path = os.path.expanduser('~/imperial_network/dawn_report_enhanced.sh')
            result = subprocess.run([script_path], capture_output=True, text=True, shell=True)
            output = result.stdout
            
            status = {
                "wealth": "269.9B",
                "gain": "238M",
                "ports": "51/51",
                "lithium": "5.2",
                "lithium_price": "275",
                "gold": "50.8",
                "beira": "14.2",
                "momo_count": "156",
                "momo_vol": "78.0"
            }
            
            for line in output.split('\n'):
                if 'TRUE VALUATION' in line:
                    wealth = re.search(r'R([\d.]+)', line)
                    if wealth:
                        val = float(wealth.group(1)) / 1e9
                        status['wealth'] = f"{val:.1f}B"
                elif 'Gain:' in line:
                    gain = re.search(r'R([\d.]+)', line)
                    if gain:
                        val = float(gain.group(1)) / 1e6
                        status['gain'] = f"{val:.0f}M"
                elif '🟢 ONLINE' in line:
                    # Count ports if needed
                    pass
            
            self.wfile.write(json.dumps(status).encode())
        
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    port = 8089  # Free port (not in dawn report)
    server = HTTPServer(('0.0.0.0', port), CEOHandler)
    print(f"🏛️ CEO Mobile View: http://localhost:{port}/ceo")
    print(f"📱 Optimized for phone screens")
    server.serve_forever()
