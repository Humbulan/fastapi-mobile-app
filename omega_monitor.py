#!/usr/bin/env python3
"""
Imperial Omega Monitor - Port 5001 (Avoids conflicts)
"""

import json
import subprocess
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

class OmegaHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Imperial Command Center</title>
                <style>
                    body {{ background: #0a0a0f; color: #00ff00; font-family: monospace; padding: 40px; }}
                    .container {{ max-width: 800px; margin: 0 auto; background: #1a1a2e; border: 1px solid #00ff00; padding: 30px; border-radius: 12px; }}
                    h1 {{ color: #ffd700; }}
                    .status {{ color: #00ff00; font-weight: bold; }}
                    .endpoint {{ background: #0f0f1a; padding: 10px; margin: 10px 0; border-left: 3px solid #00ff00; }}
                    a {{ color: #00ff00; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🏛️ IMPERIAL OMEGA</h1>
                    <p class="status">⚡ SOVEREIGN ACTIVE ⚡</p>
                    <p>Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <hr>
                    <h3>📡 Available Endpoints:</h3>
                    <div class="endpoint">
                        <strong>Health Check:</strong><br>
                        <a href="/api/health">/api/health</a>
                    </div>
                    <div class="endpoint">
                        <strong>Metrics (JSON):</strong><br>
                        <a href="/api/metrics">/api/metrics</a>
                    </div>
                    <div class="endpoint">
                        <strong>Dashboard:</strong><br>
                        <a href="http://localhost:1880/ui">http://localhost:1880/ui</a>
                    </div>
                    <hr>
                    <small>Imperial Omega Sovereign Intelligence System | Port 5001</small>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            
        elif self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'status': 'SOVEREIGN_ACTIVE',
                'timestamp': datetime.now().isoformat(),
                'uptime_seconds': int(time.time() - self.server.start_time) if hasattr(self.server, 'start_time') else 0,
                'service': 'Imperial Omega Monitor'
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif self.path == '/api/metrics' or self.path == '/metrics':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            # Get live data from Node-RED
            try:
                result = subprocess.run(
                    ['curl', '-s', 'http://127.0.0.1:1880/village_data'],
                    capture_output=True, text=True, timeout=2
                )
                if result.stdout:
                    data = json.loads(result.stdout)
                    villages = data.get('village_impact', {}).get('total_villages', 43)
                else:
                    villages = 43
            except:
                villages = 43
            
            response = {
                'timestamp': datetime.now().isoformat(),
                'valuation': 269.9,
                'villages': villages,
                'target': 500,
                'progress': '53.98%',
                'status': 'ACTIVE',
                'metrics': {
                    'daily_growth': '2.3%',
                    'weekly_growth': '15.7%',
                    'monthly_growth': '68.4%'
                }
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def log_message(self, format, *args):
        # Only log errors
        if '404' not in str(args):
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0] if args else format}")

class OmegaServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = time.time()

def run():
    port = 5001
    server = OmegaServer(('0.0.0.0', port), OmegaHandler)
    print(f"🏛️ Imperial Omega Monitor running on port {port}")
    print(f"   Root: http://localhost:{port}/")
    print(f"   Health: http://localhost:{port}/api/health")
    print(f"   Metrics: http://localhost:{port}/api/metrics")
    print("Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Monitor stopped")

if __name__ == '__main__':
    run()
