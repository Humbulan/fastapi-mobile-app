import os
import time
import subprocess
import json
from flask import Flask, jsonify, Response
from datetime import datetime

app = Flask(__name__)
start_time = time.time()

def get_live_metrics():
    try:
        # Pull directly from the Imperial Omega Node-RED stack
        res = subprocess.run(['curl', '-s', 'http://127.0.0.1:1880/village_data'], 
                           capture_output=True, text=True, timeout=2)
        return json.loads(res.stdout)
    except:
        return {"valuation": 269.9, "villages": 43, "status": "offline_fallback"}

@app.route('/api/health')
def health():
    return jsonify({
        "status": "SOVEREIGN_ACTIVE",
        "uptime": f"{int(time.time() - start_time)}s",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/metrics')
def metrics_json():
    data = get_live_metrics()
    return jsonify(data)

@app.route('/metrics')
def prometheus():
    data = get_live_metrics()
    val = data.get('valuation', 269.9)
    vil = data.get('village_impact', {}).get('total_villages', 43)
    out =  f"imperial_valuation {val}\n"
    out += f"imperial_villages {vil}\n"
    return Response(out, mimetype='text/plain')

if __name__ == '__main__':
    # Force port 5000, visible to local network
    app.run(host='0.0.0.0', port=5000, debug=False)
