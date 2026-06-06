#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from datetime import datetime

# CEO: Using Absolute Path for Imperial Direct
VAULT_PATH = os.path.expanduser("~/imperial_network/intel")
LOG_PATH = os.path.expanduser("~/imperial_network/logs/intel_notary.log")

class IntelNotaryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        files = []
        if os.path.exists(VAULT_PATH):
            files = [f for f in os.listdir(VAULT_PATH) if os.path.isfile(os.path.join(VAULT_PATH, f))]
        
        # LOG THE ACCESS (The Notary Action)
        with open(LOG_PATH, "a") as log:
            log.write(f"[{datetime.now()}] INTEL_ACCESS: {len(files)} Authority Docs Verified.\n")
        
        response = {
            'service': 'Intel_Files_Notary',
            'status': 'online',
            'classification': 'TOP SECRET',
            'files': files[:10],
            'total_files': len(files),
            'notary_log': '~/imperial_network/logs/intel_notary.log',
            'timestamp': str(datetime.now())
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())

    def log_message(self, format, *args):
        return

print("📁 Intel Notary starting on port 8191...")
HTTPServer(('0.0.0.0', 8191), IntelNotaryHandler).serve_forever()
