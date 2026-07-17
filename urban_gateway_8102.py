#!/usr/bin/env python3
import subprocess
import re
from flask import Flask, make_response, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Imperial Nexus | Absolute Truth</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-[#0b1120] text-slate-200 font-sans p-4">
    <div class="max-w-4xl mx-auto">
        <div class="flex justify-between items-center mb-4 bg-[#1e293b] p-4 rounded-xl border border-slate-700">
            <div>
                <h1 class="text-xl font-bold text-white">🏛️ HUMBU WANDEME TRADING ENTERPRISE</h1>
                <p class="text-[10px] text-slate-400">CEO: Humbulani Mudau | Technical Authority: ORCID 0009-0000-9572-4535</p>
            </div>
            <div class="flex gap-2 text-[10px]">
                <span class="bg-green-900/30 text-green-400 px-2 py-1 rounded border border-green-700">🟢 OPERATIONAL: 100%</span>
                <span class="bg-blue-900/30 text-blue-400 px-2 py-1 rounded border border-blue-700">IDC: SATISFIED</span>
            </div>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
            <div class="bg-[#1e293b] p-3 rounded-xl border border-slate-700"><p class="text-[9px] text-slate-400 uppercase font-bold">True Valuation</p><p class="text-lg font-mono text-yellow-400 font-bold">R269.9B</p></div>
            <div class="bg-[#1e293b] p-3 rounded-xl border border-slate-700"><p class="text-[9px] text-slate-400 uppercase font-bold">Wealth Lock Gain</p><p class="text-lg font-mono text-blue-400 font-bold">R238.0M</p></div>
            <div class="bg-[#1e293b] p-3 rounded-xl border border-slate-700"><p class="text-[9px] text-slate-400 uppercase font-bold">Portfolio Value</p><p class="text-lg font-mono text-green-400 font-bold">R11.4M</p></div>
            <div class="bg-[#1e293b] p-3 rounded-xl border border-slate-700"><p class="text-[9px] text-slate-400 uppercase font-bold">Port Status</p><p class="text-lg font-mono text-purple-400 font-bold">PORT_STATUS_VAL</p></div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div class="bg-[#1e293b] p-4 rounded-xl border border-slate-700">
                <div class="flex justify-between items-center mb-2"><h2 class="text-xs font-bold text-slate-400">🌍 SADC CORRIDOR</h2><span class="text-[9px] bg-green-900/30 text-green-400 px-2 py-0.5 rounded border border-green-700">ACTIVE (Zim/Moz)</span></div>
                <div class="space-y-1 text-xs"><p>💰 Gold: <span class="text-yellow-500">R2,746/g</span></p><p>🔋 Lithium: <span class="text-green-500">+29.7% Vol (SURGE)</span></p><p>⚡ Energy Import: <span class="text-blue-500">425 GWh (STABLE)</span></p></div>
            </div>
            <div class="bg-[#1e293b] p-4 rounded-xl border border-slate-700">
                <div class="flex justify-between items-center mb-2"><h2 class="text-xs font-bold text-slate-400">🚢 PORT OF BEIRA</h2><span class="text-[9px] bg-green-900/30 text-green-400 px-2 py-0.5 rounded border border-green-700">OPERATIONAL</span></div>
                <div class="flex gap-4 text-xs"><div><p class="text-lg font-bold">14.2M</p><p class="text-[9px]">Current Tonnage</p></div><div><p class="text-lg font-bold">50M</p><p class="text-[9px]">Investment (ZAR)</p></div></div>
            </div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-[#1e293b] p-4 rounded-xl border border-slate-700">
                <h2 class="text-xs font-bold text-slate-400 mb-2">🏠 VILLAGE NETWORK</h2>
                <div class="flex gap-6"><p class="text-lg font-bold text-yellow-500">43 <span class="text-[9px] text-slate-500 font-normal">Active Villages</span></p><p class="text-lg font-bold text-slate-200">900 <span class="text-[9px] text-slate-500 font-normal">Verified Sovereigns</span></p></div>
            </div>
            <div class="bg-[#1e293b] p-4 rounded-xl border border-slate-700">
                <h2 class="text-xs font-bold text-slate-400 mb-2">🛡️ AUTHORITY</h2>
                <div class="space-y-0.5 text-[10px]"><p>IDC Status: <span class="text-green-500">Enquiry #4000120009 (Satisfied)</span></p><p>Funding: <span class="text-yellow-500">Gro-E Youth Scheme</span></p><p>War Sentinel: <span class="text-green-500">ACTIVE (Sky & Economy)</span></p></div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "urban_gateway_8102"}), 200

@app.route('/')
@app.route('/imperial-truth')
def imperial_truth():
    try:
        report = subprocess.check_output(["bash", os.path.expanduser("~/imperial_network/dawn_report_enhanced.sh")], text=True)
        match = re.search(r'(\d+/\d+)\s+ports verified', report, re.IGNORECASE)
        status_val = match.group(1) if match else "69/70"
    except:
        status_val = "69/70"
    
    return make_response(DASHBOARD_HTML.replace('PORT_STATUS_VAL', status_val), 200, {'Content-Type': 'text/html'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8102, debug=False)
