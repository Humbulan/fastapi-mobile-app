#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
import os

class SurgeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        try:
            # Android-compatible metrics
            with open('/proc/loadavg', 'r') as f:
                load = f.read().strip().split()[0]
            
            with open('/proc/meminfo', 'r') as f:
                mem_total = int(f.readline().split()[1])
                mem_free = int(f.readline().split()[1])
                mem_used = mem_total - mem_free
            
            response = {
                "port": 8104,
                "service": "Surge Monitor",
                "cpu_load": float(load),
                "memory_used_mb": mem_used / 1024,
                "memory_total_mb": mem_total / 1024,
                "timestamp": time.time()
            }
        except:
            response = {"port": 8104, "status": "running", "timestamp": time.time()}
        
        self.wfile.write(json.dumps(response).encode())

if __name__ == '__main__':
    print("🚀 Surge Monitor starting on port 8104...")
    server = HTTPServer(('0.0.0.0', 8104), SurgeHandler)
    server.serve_forever()
