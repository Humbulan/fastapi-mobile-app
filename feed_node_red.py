#!/usr/bin/env python3
import requests
import subprocess
import time
import re

def update_dashboard():
    try:
        # Run dawn report
        result = subprocess.run(['~/imperial_network/dawn_report_enhanced.sh'], 
                              capture_output=True, text=True, shell=True)
        output = result.stdout
        
        # Extract wealth (R269,905,078,380.45 -> 269.9B)
        wealth_match = re.search(r'TRUE VALUATION:\s+R([\d.]+)', output)
        if wealth_match:
            wealth = float(wealth_match.group(1)) / 1e9
            print(f"💰 Wealth: {wealth:.1f}B")
            # Trigger wealth gauge
            requests.post("http://localhost:1880/inject/node_wealth_inject", 
                        json={"payload": wealth})
        
        # Count online ports
        online = output.count("🟢 ONLINE")
        print(f"🛡️ Ports: {online}/51")
        # Trigger ports display
        requests.post("http://localhost:1880/inject/node_ports_inject", 
                    json={"payload": online})
        
        # SADC metrics (static for now, can be parsed)
        print("🌍 SADC Corridor: Active")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("📡 Imperial Dashboard Feeder Started")
    while True:
        update_dashboard()
        time.sleep(30)
