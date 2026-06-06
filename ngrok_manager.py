#!/usr/bin/env python3
"""
ngrok Manager for Imperial Network
- Automated tunnel provisioning for new nodes
- Health monitoring for all tunnels
- Integration with dawn report
"""

import os
import json
import requests
import subprocess
from datetime import datetime

# Load credentials from secure file
def load_creds():
    creds = {}
    with open(os.path.expanduser('~/.ngrok_creds'), 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                # Split only on first = and clean up quotes
                parts = line.split('=', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip().strip('"').strip("'")
                    creds[key] = value
    return creds

CREDS = load_creds()
API_KEY = CREDS.get('NGROK_API_KEY')
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Ngrok-Version": "2",
    "Content-Type": "application/json"
}

def create_tunnel(name, region="us", port=1880):
    """Create a new reserved domain for a partner"""
    url = "https://api.ngrok.com/reserved_domains"
    data = {
        "name": f"{name}.humbu.store",
        "region": region,
        "description": f"Imperial tunnel for {name} - Port {port}"
    }
    
    try:
        response = requests.post(url, headers=HEADERS, json=data)
        if response.status_code in [200, 201]:
            print(f"✅ Created tunnel: {name}.humbu.store")
            return response.json()
        else:
            print(f"❌ Failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def list_tunnels():
    """List all active tunnels"""
    url = "https://api.ngrok.com/tunnels"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def check_health():
    """Check health of all tunnels and report to dawn report"""
    try:
        tunnels = list_tunnels()
        online = 0
        total = len(tunnels.get('tunnels', []))
        
        print("\n📡 NGROK TUNNEL STATUS")
        print("=" * 50)
        for tunnel in tunnels.get('tunnels', []):
            name = tunnel.get('name', 'unknown')
            public_url = tunnel.get('public_url', '')
            status = "🟢 ONLINE" if public_url else "🔴 OFFLINE"
            if public_url:
                online += 1
            print(f"{status} | {name}: {public_url}")
        
        print("=" * 50)
        print(f"📊 TUNNELS: {online}/{total} online")
        return online, total
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return 0, 0

def restart_tunnel(port):
    """Restart a tunnel by killing and recreating"""
    # Kill existing tunnel on that port
    subprocess.run(f"pkill -f 'ngrok.*{port}'", shell=True, stderr=subprocess.DEVNULL)
    
    # Start new tunnel
    subprocess.Popen(f"nohup ngrok http {port} > logs/ngrok_{port}.log 2>&1 &", 
                     shell=True, 
                     stdout=subprocess.DEVNULL, 
                     stderr=subprocess.DEVNULL)
    print(f"🔄 Restarted tunnel on port {port}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "create" and len(sys.argv) > 2:
            create_tunnel(sys.argv[2])
        elif sys.argv[1] == "list":
            tunnels = list_tunnels()
            print(json.dumps(tunnels, indent=2))
        elif sys.argv[1] == "health":
            check_health()
        elif sys.argv[1] == "restart" and len(sys.argv) > 2:
            restart_tunnel(sys.argv[2])
    else:
        check_health()
