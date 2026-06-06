from flask import Flask, jsonify
import subprocess
import requests

app = Flask(__name__)

def get_live_market(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=5)
        data = r.json()
        return data['chart']['result'][0]['meta']['regularMarketPrice']
    except:
        return "N/A"

@app.route('/imperial-stats', methods=['GET'])
def get_stats():
    try:
        cmd = "bash /data/data/com.termux/files/home/imperial_network/dawn_report_enhanced.sh"
        local_stats = subprocess.check_output(cmd, shell=True).decode('utf-8')
        
        return jsonify({
            "status": "SUCCESS",
            "market_prices": {
                "Gold (JSE:SSW)": get_live_market("SSW.JO"),
                "ZAR_USD": get_live_market("USDZAR=X")
            },
            "live_data": local_stats
        })
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8121)
