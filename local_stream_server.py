import subprocess
import re
import json
from datetime import datetime, UTC
from http.server import HTTPServer, BaseHTTPRequestHandler

def run_live_parse():
    """Executes the infrastructure report and returns the active payload dict"""
    result = subprocess.run(['/bin/bash', 'dawn_report_enhanced.sh'], capture_output=True, text=True)
    output = result.stdout
    try:
        portfolio_val = float(re.search(r"PORTFOLIO VALUE:\s*R([\d\.]+)", output).group(1))
        progress_val = float(re.search(r"PROGRESS TO R500B:\s*([\d\.]+)%", output).group(1))
        ports_verified = int(re.search(r"STATUS:\s*(\d+)/\d+\s*ports verified", output).group(1))

        trade_volume_str = re.search(r"TRADE VOLUME:\s*R([\d,\.]+)", output).group(1)
        trade_volume = float(trade_volume_str.replace(',', ''))

        gold_monthly = float(re.search(r"GOLD EXPORTS:.*Monthly:\s*([\d\.]+)M", output, re.DOTALL).group(1))
        current_time = datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

        return [{
            "timestamp": current_time,
            "portfolio_value": portfolio_val,
            "progress_percentage": progress_val,
            "active_ports": ports_verified,
            "sadc_trade_volume": trade_volume,
            "gold_monthly_m": gold_monthly
        }]
    except Exception as e:
        return {"error": f"Live infrastructure parsing anomaly: {str(e)}"}

class DynamicStreamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/stream':
            # Run the parser dynamically on request arrival
            payload = run_live_parse()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(payload, indent=2).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 8130), DynamicStreamHandler)
    print("[*] Imperial Stream Engine initialized on http://localhost:8130/stream")
    server.serve_forever()
