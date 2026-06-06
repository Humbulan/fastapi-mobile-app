#!/usr/bin/env python3
"""
Simple Ukuvuselela Webhook - No complex imports
"""
import json
import os
import sys
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# Gauteng readiness tracker
gauteng_score = {
    "previous": 6.9,
    "current": 8.5,
    "target": 8.5,
    "last_update": datetime.now().isoformat(),
    "metrics": {
        "city_deep_throughput": 0,
        "midrand_throughput": 0,
        "kaalfontein_throughput": 0,
        "total_shipments": 0,
        "lithium_shipments": 0
    }
}

class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'status': 'online',
                'service': 'ukuvuselela_webhook',
                'gauteng_score': gauteng_score['current'],
                'target': gauteng_score['target']
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/api/metrics':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(gauteng_score).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/webhooks/rail-manifest':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data)
                manifest = data.get('manifest', {})
                
                # Extract details
                manifest_id = manifest.get('manifest_id', 'unknown')
                commodity = manifest.get('commodity_code', '')
                tonnage = float(manifest.get('gross_tonnage', 0))
                terminal = manifest.get('origin_terminal', 'unknown')
                
                # Update metrics
                gauteng_score['metrics']['total_shipments'] += 1
                
                if terminal == 'city_deep':
                    gauteng_score['metrics']['city_deep_throughput'] += tonnage
                elif terminal == 'midrand':
                    gauteng_score['metrics']['midrand_throughput'] += tonnage
                elif terminal == 'kaalfontein':
                    gauteng_score['metrics']['kaalfontein_throughput'] += tonnage
                
                # Check for lithium
                if commodity == '2616' or 'lithium' in str(manifest).lower():
                    gauteng_score['metrics']['lithium_shipments'] += 1
                    print(f"🔋 LITHIUM PREMIUM: {manifest_id}")
                
                # Update score
                self.update_gauteng_score()
                
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {
                    'status': 'processed',
                    'manifest_id': manifest_id,
                    'gauteng_score': gauteng_score['current']
                }
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                print(f"Error: {e}")
        else:
            self.send_response(404)
            self.end_headers()
    
    def update_gauteng_score(self):
        """Calculate Gauteng readiness score"""
        metrics = gauteng_score['metrics']
        
        total_throughput = (
            metrics['city_deep_throughput'] +
            metrics['midrand_throughput'] +
            metrics['kaalfontein_throughput']
        )
        
        # Score calculation
        throughput_score = min(total_throughput / 10000, 1.2)
        customs_score = 0.92 * 0.4  # Fixed customs rate
        shipment_bonus = min(metrics['total_shipments'] / 50, 0.3)
        lithium_bonus = min(metrics['lithium_shipments'] * 0.05, 0.2)
        
        new_score = 6.9 + throughput_score + customs_score + shipment_bonus + lithium_bonus
        gauteng_score['current'] = min(new_score, 8.5)
        gauteng_score['last_update'] = datetime.now().isoformat()
        
        if gauteng_score['current'] >= 8.5:
            print("\n🎯 GAUTENG TARGET ACHIEVED: 8.5!")
    
    def log_message(self, format, *args):
        # Suppress log messages
        pass

def run_server(port=8117):
    server_address = ('', port)
    httpd = HTTPServer(server_address, WebhookHandler)
    print(f"\n{'='*50}")
    print(f"🚂 Ukuvuselela Webhook running on port {port}")
    print(f"{'='*50}")
    print(f"📊 Initial Score: {gauteng_score['current']}/8.5")
    print(f"🎯 Target: 8.5")
    print(f"{'='*50}")
    print(f"Press Ctrl+C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n\n👋 Server stopped")
        print(f"📊 Final Score: {gauteng_score['current']}/8.5")

if __name__ == '__main__':
    run_server()
