from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Imperial Live Metrics</title>
    <meta http-equiv="refresh" content="30">
    <style>
        body { font-family: 'Segoe UI', monospace; background: #0a0a0f; color: #00ff00; padding: 20px; }
        .card { background: #1a1a2e; border: 1px solid #00ff00; border-radius: 12px; padding: 25px; box-shadow: 0 4px 15px rgba(0,255,0,0.1); }
        h1 { color: #ffd700; border-bottom: 1px solid #333; padding-bottom: 10px; }
        .metrics-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; margin-top: 20px; }
        .metric { background: #0f0f1a; padding: 15px; border-radius: 8px; border-left: 3px solid #ffd700; }
        .value { font-size: 22px; font-weight: bold; color: #ffffff; display: block; margin-top: 5px; }
        .label { font-size: 12px; text-transform: uppercase; color: #888; }
        hr { border: 0; border-top: 1px solid #333; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🏛️ Imperial Real‑Time Metrics</h1>
        <div id="metrics" class="metrics-grid">Loading telemetry...</div>
        <hr>
        <small>System: Imperial Nexus | Status: Active | Refresh: 30s</small>
    </div>
    <script>
        function fetchMetrics() {
            fetch('/api/metrics')
                .then(res => res.json())
                .then(data => {
                    let html = '';
                    for (let key in data) {
                        let label = key.replace(/_/g, ' ').toUpperCase();
                        html += `<div class="metric">
                                    <span class="label">${label}</span>
                                    <span class="value">${data[key]}</span>
                                 </div>`;
                    }
                    document.getElementById('metrics').innerHTML = html;
                })
                .catch(err => {
                    document.getElementById('metrics').innerHTML = '<p style="color:red">Error: Could not connect to API</p>';
                });
        }
        fetchMetrics();
        setInterval(fetchMetrics, 30000);
    </script>
</body>
</html>
'''

@app.route('/')
def dashboard():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/metrics')
def metrics_proxy():
    try:
        resp = requests.get('http://127.0.0.1:5006/api/metrics', timeout=5)
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=False)
