from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/api/value')
def value():
    return jsonify({"portfolio_value": 269911161297.38, "progress": 53.98})

@app.route('/api/wealth_lock')
def wealth_lock():
    return jsonify({"gain": 238050000, "status": "active"})

@app.route('/api/volume')
def volume():
    return jsonify({"sadc_volume": 5017500, "unit": "ZAR"})

@app.route('/api/lithium')
def lithium():
    return jsonify({"price": 275, "monthly_export": 5.2e6, "trend": "bullish"})

@app.route('/api/summary')
def summary():
    return jsonify({"bi": "All corridors operational"})

@app.route('/api/status')
def status():
    return jsonify({"services": 59, "health": "green"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8124)
