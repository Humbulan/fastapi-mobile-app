#!/usr/bin/env python3
"""
Webhook with Prometheus metrics – names match Imperial dashboard.
Now also proxies Cloudflare metrics with caching.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import datetime
import json
import urllib.request
import threading
import time

# Global cache for Cloudflare metrics
cf_cache = {
    'data': '',
    'timestamp': 0,
    'ttl': 60  # seconds
}

def refresh_cloudflare_metrics():
    """Fetch Cloudflare metrics and update cache."""
    global cf_cache
    req = urllib.request.Request(
        "https://humbu.store/metrics",
        headers={"User-Agent": "curl/8.0.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            cf_cache['data'] = resp.read().decode()
            cf_cache['timestamp'] = time.time()
    except Exception as e:
        cf_cache['data'] = f'# ERROR fetching Cloudflare metrics: {str(e)}\n'
        cf_cache['timestamp'] = time.time()

# Run the refresh in a background thread
def background_refresh():
    while True:
        refresh_cloudflare_metrics()
        time.sleep(cf_cache['ttl'])

thread = threading.Thread(target=background_refresh, daemon=True)
thread.start()

class WebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == '/metrics':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; version=0.0.4')
            self.end_headers()

            # Core metrics – named to match dashboard queries
            metrics = (
                '# HELP imperial_valuation Total portfolio valuation\n'
                '# TYPE imperial_valuation gauge\n'
                'imperial_valuation 269911162347.394526875\n'
                '# HELP imperial_wealth_gain Market gain\n'
                '# TYPE imperial_wealth_gain gauge\n'
                'imperial_wealth_gain 238050000\n'
                '# HELP imperial_gold_price Gold price in R/g\n'
                '# TYPE imperial_gold_price gauge\n'
                'imperial_gold_price 2746\n'
                '# HELP imperial_energy_flow Energy price in $/MWh\n'
                '# TYPE imperial_energy_flow gauge\n'
                'imperial_energy_flow 9.2\n'
                '# HELP imperial_grid_status Gauteng power grid status\n'
                '# TYPE imperial_grid_status gauge\n'
                'imperial_grid_status 1\n'
                '# HELP imperial_progress Progress to R500B\n'
                '# TYPE imperial_progress gauge\n'
                'imperial_progress 53.98\n'
                '# HELP imperial_lithium_flow Lithium price\n'
                '# TYPE imperial_lithium_flow gauge\n'
                'imperial_lithium_flow 275\n'
                '# HELP imperial_beira_status Port of Beira capacity\n'
                '# TYPE imperial_beira_status gauge\n'
                'imperial_beira_status 14.2\n'
                '# HELP imperial_port_status Overall port status\n'
                '# TYPE imperial_port_status gauge\n'
                'imperial_port_status 1\n'
            )

            # Response times (keep as is)
            mock_times = {
                'IMPERIAL_WEB_UPGRADE': 0.23,
                'SADC_A_LOGISTICS': 0.45,
                'SADC_B_RETAIL': 0.38,
                'Node-RED': 0.12,
                'Prometheus': 0.08,
                'Metrics_API': 0.31,
            }
            for service, value in mock_times.items():
                metrics += f'response_time_seconds{{service="{service}"}} {value}\n'

            # Append cached Cloudflare metrics
            metrics += cf_cache['data']

            self.wfile.write(metrics.encode())
            self.log_to_file('GET', self.path)
            return

        # Original GET behaviour (health check)
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Ukuvuselela Webhook Active')
        self.log_to_file('GET', self.path)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "received"}).encode())
        self.log_to_file('POST', self.path, body)

    def log_to_file(self, method, path, body=''):
        log_line = f"{datetime.datetime.now().isoformat()} {method} {path}"
        if body:
            log_line += f" body: {body[:200]}"
        with open('/data/data/com.termux/files/home/imperial_network/logs/ukuvo_webhook.log', 'a') as f:
            f.write(log_line + '\n')

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8117), WebhookHandler)
    print("Webhook listening on port 8117")
    server.serve_forever()
