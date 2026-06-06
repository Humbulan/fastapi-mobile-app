#!/usr/bin/env python3
"""
Voucher API Service - Port 8098
Handles voucher activation and management for Imperial Omega
"""
from flask import Flask, request, jsonify, render_template_string
import json
import os
from datetime import datetime
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# HTML template for the root page
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Imperial AI - Voucher Activation</title>
    <style>
        body { font-family: Arial; padding: 40px; background: #f5f5f5; }
        .container { max-width: 500px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        input, button { padding: 10px; margin: 5px; width: 100%; }
        .success { color: green; }
        .error { color: red; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🎫 Activate AI Access</h2>
        <p>Enter your voucher code (format: XXXX-XXXX)</p>
        <input type="text" id="code" placeholder="e.g., ABCD-1234">
        <button onclick="activate()">Activate</button>
        <div id="result"></div>
    </div>
    <script>
        function activate() {
            let code = document.getElementById('code').value;
            fetch('/api/activate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({code: code})
            })
            .then(r => r.json())
            .then(d => {
                let div = document.getElementById('result');
                if(d.success) {
                    div.innerHTML = '<p class="success">✅ ' + d.message + '</p>';
                } else {
                    div.innerHTML = '<p class="error">❌ ' + d.message + '</p>';
                }
            });
        }
    </script>
</body>
</html>
'''

def load_vouchers():
    """Load vouchers from JSON file"""
    try:
        with open('/data/data/com.termux/files/home/imperial_network/vouchers.json') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Vouchers file not found")
        return {}
    except json.JSONDecodeError:
        logger.error("Invalid JSON in vouchers file")
        return {}

def save_vouchers(vouchers):
    """Save vouchers to JSON file"""
    with open('/data/data/com.termux/files/home/imperial_network/vouchers.json', 'w') as f:
        json.dump(vouchers, f, indent=2)

@app.route('/')
def index():
    """Serve the activation page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/activate', methods=['POST'])
def activate():
    """Activate a voucher code"""
    data = request.get_json()
    code = data.get('code', '').upper().strip()
    
    vouchers = load_vouchers()
    
    if code in vouchers:
        voucher = vouchers[code]
        if voucher.get('status') == 'active':
            # Mark as used
            voucher['status'] = 'used'
            voucher['redeemed_at'] = datetime.now().isoformat()
            save_vouchers(vouchers)
            return jsonify({
                'success': True,
                'message': f'Voucher activated! Value: R{voucher["value"]}'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Voucher already used or expired'
            })
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid code'
        })

@app.route('/api/validate', methods=['POST'])
def validate():
    """Validate a voucher without activating"""
    data = request.get_json()
    code = data.get('code', '').upper().strip()
    
    vouchers = load_vouchers()
    
    if code in vouchers:
        voucher = vouchers[code]
        return jsonify({
            'valid': voucher.get('status') == 'active',
            'value': voucher.get('value', 0),
            'status': voucher.get('status')
        })
    else:
        return jsonify({'valid': False})

@app.route('/api/vouchers', methods=['GET'])
def get_vouchers():
    """Return all vouchers (for internal use)"""
    vouchers = load_vouchers()
    return jsonify(vouchers)

@app.route('/api/stats')
def stats():
    """Return voucher statistics"""
    vouchers = load_vouchers()
    total = len(vouchers)
    active = sum(1 for v in vouchers.values() if v.get('status') == 'active')
    used = sum(1 for v in vouchers.values() if v.get('status') == 'used')
    total_value = sum(v.get('value', 0) for v in vouchers.values())
    
    return jsonify({
        'total_vouchers': total,
        'active': active,
        'used': used,
        'total_value': total_value,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'port': 8098,
        'service': 'voucher-api',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🎫 Voucher API Service starting on port 8098...")
    app.run(host='127.0.0.1', port=8098, debug=False)
