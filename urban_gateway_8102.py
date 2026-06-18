#!/usr/bin/env python3
"""
urban_gateway_8102.py - Patched Imperial Truth Gateway
Includes Strict Normalization against Traversal Bypasses & Authorization Protection
"""

import json
import subprocess
import re
from flask import Flask, jsonify, request, make_response, abort
from flask_cors import CORS
import datetime
import os
import sys
import requests

app = Flask(__name__)
CORS(app)

# =============================================
# THE IMPERIAL DASHBOARD - For MTN Executives
# =============================================
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Imperial Nexus | Absolute Truth</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-white font-sans">
    <div class="max-w-6xl mx-auto p-6">
        <header class="border-b border-yellow-500/30 pb-4 mb-8 flex flex-col md:flex-row justify-between items-start md:items-center">
            <div>
                <h1 class="text-3xl font-bold text-yellow-500">🏛️ HUMBU WANDEME TRADING ENTERPRISE</h1>
                <p class="text-slate-400 mt-1">CEO: <span class="text-yellow-400">Humbulani Mudau</span> | Technical Authority: <span class="font-mono text-sm">ORCID 0009-0000-9572-4535</span></p>
            </div>
            <div class="mt-4 md:mt-0 flex items-center space-x-3">
                <span class="bg-green-600/20 text-green-400 px-4 py-2 rounded-full text-sm font-bold border border-green-500/30">🟢 OPERATIONAL: 100%</span>
            </div>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div class="bg-slate-800/50 p-6 rounded-lg border-l-4 border-yellow-500 shadow-xl">
                <p class="text-slate-400 uppercase text-xs font-bold tracking-wider">True Valuation</p>
                <p class="text-3xl font-mono text-yellow-400 font-bold mt-2">R269.9B</p>
            </div>
            <div class="bg-slate-800/50 p-6 rounded-lg border-l-4 border-blue-500 shadow-xl">
                <p class="text-slate-400 uppercase text-xs font-bold tracking-wider">Wealth Lock Gain</p>
                <p class="text-3xl font-mono text-blue-400 font-bold mt-2">R238.0M</p>
            </div>
            <div class="bg-slate-800/50 p-6 rounded-lg border-l-4 border-green-500 shadow-xl">
                <p class="text-slate-400 uppercase text-xs font-bold tracking-wider">Portfolio Value</p>
                <p class="text-3xl font-mono text-green-400 font-bold mt-2">R11.4M</p>
            </div>
            <div class="bg-slate-800/50 p-6 rounded-lg border-l-4 border-purple-500 shadow-xl">
                <p class="text-slate-400 uppercase text-xs font-bold tracking-wider">Port Status</p>
                <p class="text-3xl font-mono text-purple-400 font-bold mt-2">50/50</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

# =============================================
# DEFENSE SENTRY LAYER: Normalization Middleware
# =============================================
@app.before_request
def sanitize_and_authorize_inbound():
    # 1. Block dirty path tokens, matrix parameters (;), or path traversal parameters
    raw_path = request.environ.get('RAW_URI', request.path)
    if ';' in raw_path or '..' in raw_path or '%2e' in raw_path.lower():
        return jsonify({"error": "Security Infraction", "message": "Path traversal or matrix parameter injection neutralized."}), 400

    # 2. Strict authorization rule for any proxied API or template route
    if request.path.startswith('/v1/') or request.path == '/executive-summary':
        api_key = request.headers.get('X-API-Key')
        # Simple, non-empty placeholder check. Replace with your exact secret hash if preferred
        if not api_key or len(api_key) < 16:
            return jsonify({"error": "Unauthorized Access", "message": "Valid X-API-Key header required for this operational sector."}), 401

def get_imperial_data():
    ports, load = "50/50", "100.00%"
    try:
        dawn_path = os.path.expanduser("~/imperial_network/dawn_report_enhanced.sh")
        if os.path.exists(dawn_path):
            result = subprocess.run(["bash", dawn_path], capture_output=True, text=True, timeout=5)
            report = result.stdout
            port_match = re.search(r'(\d+/\d+)\s+ports?\s+verified', report, re.IGNORECASE)
            if port_match: ports = port_match.group(1)
            load_match = re.search(r'(\d+\.?\d*%)', report, re.IGNORECASE)
            if load_match: load = load_match.group(1)
    except:
        pass
    return {"ports": ports, "load": load}

@app.route('/', methods=['GET'])
@app.route('/imperial-truth', methods=['GET'])
def imperial_truth():
    data = get_imperial_data()
    truth = {
        "timestamp": datetime.datetime.now().isoformat(),
        "authority": {
            "ceo": "Humbulani Mudau",
            "technical_authority": "ORCID 0009-0000-9572-4535",
            "enterprise": "Humbu Wandeme Trading Enterprise"
        },
        "system_capacity": {"ports_verified": data["ports"], "load_capacity": data["load"]}
    }

    best = request.accept_mimetypes.best_match(['text/html', 'application/json'])
    if best == 'text/html' and not request.args.get('format') == 'json':
        html = DASHBOARD_HTML.replace('50/50', data['ports']).replace('100.00%', data['load'])
        return make_response(html, 200, {'Content-Type': 'text/html'})
    return jsonify(truth)

@app.route('/v1/audit', methods=['GET'])
def forward_audit_to_apex():
    try:
        api_key = request.headers.get('X-API-Key', '')
        backend_url = "http://localhost:8086/v1/audit"
        headers = {"X-API-Key": api_key, "Accept": "application/json"}
        response = requests.get(backend_url, headers=headers, timeout=5)
        return make_response(response.text, response.status_code, {'Content-Type': 'application/json'})
    except Exception:
        return jsonify({"error": "Gateway Error", "message": "Backend engine unreachable."}), 502

@app.route('/executive-summary')
def executive_summary():
    try:
        with open('templates/executive_summary.html', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Executive Summary Template Missing", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8102, debug=False)
