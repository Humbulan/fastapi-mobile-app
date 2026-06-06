from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Path to your voucher audit file
AUDIT_FILE = os.path.expanduser('~/imperial_network/data/sez_voucher_audit.json')

@app.route('/api/metrics')
def metrics():
    try:
        if os.path.exists(AUDIT_FILE):
            with open(AUDIT_FILE, 'r') as f:
                return jsonify(json.load(f))
        return jsonify({"status": "Voucher Data Pending", "sez": "Nkomazi"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({
        "status": "ONLINE",
        "system": "IMPERIAL OMEGA",
        "port": 8117,
        "integrity": "VERIFIED"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8117)
