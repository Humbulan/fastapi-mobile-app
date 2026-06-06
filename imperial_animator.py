from flask import Flask, request
import time
import sys
import json
import os
from datetime import datetime

app = Flask(__name__)

LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

def log_trigger(data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = os.path.join(LOG_DIR, f"jira_triggers_{datetime.now().strftime('%Y%m%d')}.log")
    
    # Handle different data types
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except:
            data = {"raw": data}
    elif data is None:
        data = {}
    
    # Extract issue key safely
    issue_key = "Unknown"
    if isinstance(data, dict):
        # Try different possible JSON structures
        if 'issue' in data and isinstance(data['issue'], dict):
            issue_key = data['issue'].get('key', 'No key')
        elif 'key' in data:
            issue_key = data['key']
        elif 'issue_key' in data:
            issue_key = data['issue_key']
        else:
            issue_key = str(data)[:50]
    
    # Log it
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] Triggered by: {issue_key}\n")
        if isinstance(data, dict):
            f.write(f"Data keys: {list(data.keys())}\n")
    
    return issue_key

def play_animation(issue_key=None):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    colors = ["\033[92m", "\033[93m", "\033[94m", "\033[95m"]
    
    print(f"\n{'='*50}")
    print(f"[JIRA TRIGGER RECEIVED] {datetime.now().strftime('%H:%M:%S')}")
    if issue_key:
        print(f"[ISSUE] {issue_key}")
    print(f"{'='*50}")
    
    for cycle in range(3):
        color = colors[cycle % len(colors)]
        for frame in frames:
            status_msg = "Synchronizing Jira Settings"
            if issue_key:
                status_msg += f" - {issue_key}"
            sys.stdout.write(f"\r{color}{frame} {status_msg}...\033[0m")
            sys.stdout.flush()
            time.sleep(0.1)
    
    print(f"\n\033[92m✓ Terminal heartbeat confirmed - Process protected\033[0m")
    print(f"{'='*50}\n")

@app.route('/jira-sync', methods=['POST'])
def webhook():
    # Get raw data and try multiple parsing methods
    raw_data = request.get_data(as_text=True)
    print(f"\n[DEBUG] Raw data received: {raw_data[:100]}")  # Debug line
    
    # Try to parse JSON
    data = None
    try:
        data = request.get_json()
    except:
        pass
    
    # If that fails, try manual parsing
    if data is None and raw_data:
        try:
            data = json.loads(raw_data)
        except:
            data = {"raw": raw_data}
    
    # If still nothing, use empty dict
    if data is None:
        data = {}
    
    issue_key = log_trigger(data)
    play_animation(issue_key)
    return {"status": "animation_complete", "issue": issue_key}, 200

@app.route('/health', methods=['GET'])
def health():
    return {"status": "alive", "message": "Imperial Animator is running"}, 200

if __name__ == '__main__':
    PORT = 8120
    print(f"\033[92m╔══════════════════════════════════════╗")
    print(f"║   IMPERIAL ANIMATOR ACTIVATED       ║")
    print(f"║   Listening for Jira webhooks...    ║")
    print(f"║   Port: {PORT}                           ║")
    print(f"╚══════════════════════════════════════╝\033[0m")
    print(f"\nServer starting on http://0.0.0.0:{PORT}")
    app.run(host='0.0.0.0', port=PORT, threaded=True)
