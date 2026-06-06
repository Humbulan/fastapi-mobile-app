from flask import Flask
import threading
import time
import datetime

app = Flask(__name__)

# Imperial Sovereign Thresholds
DATA = {
    "status": "Sovereign Shield Active",
    "valuation": "R269.9B",
    "integrity": "100%",
    "last_check": ""
}

@app.route('/')
def home():
    return f"""
    <html>
    <body style="background:#000; color:#0f0; font-family:monospace; padding:20px;">
        <h1>🛡️ SENTINEL 8105: ACTIVE</h1>
        <hr>
        <p>STATUS: {DATA['status']}</p>
        <p>VALUATION: {DATA['valuation']}</p>
        <p>INTEGRITY: {DATA['integrity']}</p>
        <p>LAST PULSE: {DATA['last_check']}</p>
    </body>
    </html>
    """

def monitor_loop():
    while True:
        DATA['last_check'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Logic for checking Gold/Grid goes here
        time.sleep(60)

if __name__ == "__main__":
    # Start the logic in a background thread
    threading.Thread(target=monitor_loop, daemon=True).start()
    # Start the web server on 8105
    app.run(port=8105, host='0.0.0.0')
