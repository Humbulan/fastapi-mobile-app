#!/usr/bin/env python3
import json
import http.server
import socketserver
import os

PORT = 8110
FLOW_FILE = os.path.expanduser("~/.node-red/flows.json")

class MetricsHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            try:
                with open(FLOW_FILE, 'r') as f:
                    data = json.load(f)
                tabs = [obj for obj in data if obj.get('type') == 'tab']
                flow_count = len(tabs)
                nodes = [obj for obj in data if obj.get('z') and obj.get('type') != 'tab']
                node_count = len(nodes)
                metrics = (
                    "# HELP node_red_flow_count Number of flows (tabs)\n"
                    "# TYPE node_red_flow_count gauge\n"
                    f"node_red_flow_count {flow_count}\n"
                    "# HELP node_red_node_count Total number of nodes\n"
                    "# TYPE node_red_node_count gauge\n"
                    f"node_red_node_count {node_count}\n"
                )
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain; version=0.0.4')
                self.end_headers()
                self.wfile.write(metrics.encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"ERROR: {e}".encode())
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Not Found")

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), MetricsHandler) as httpd:
        print(f"Serving Node-RED metrics on port {PORT}")
        httpd.serve_forever()
