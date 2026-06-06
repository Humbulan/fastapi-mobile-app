#!/usr/bin/env python3
import json
import time
import random
import requests
from datetime import datetime

def generate_village_data():
    """Generate dynamic village impact data with trends"""
    base_villages = {
        "Thohoyandou/Sibasa": {"current": 18, "growth": 28.5},
        "Malamulele": {"current": 14, "growth": 40.0},
        "Nkomazi SEZ Corridor": {"current": 11, "growth": 37.5}
    }
    
    # Add some variation to show real-time changes
    for region in base_villages:
        variation = random.uniform(-0.5, 0.5)
        base_villages[region]["growth"] = round(base_villages[region]["growth"] + variation, 1)
        
    return {
        "timestamp": datetime.now().isoformat(),
        "village_impact": {
            "total_villages": 43,
            "regions": [
                {"name": k, "current": v["current"], "growth": v["growth"]}
                for k, v in base_villages.items()
            ],
            "status": "Sovereign"
        },
        "mineral_data": {
            "lithium": {
                "value": f"R{random.randint(4100, 4300)}/t",
                "trend": f"+{random.uniform(27, 30):.1f}%",
                "status": "SURGING"
            },
            "gold": {
                "value": f"R{random.uniform(1.18, 1.22):.2f}M/kg",
                "trend": f"+{random.uniform(4.5, 6.5):.1f}%",
                "status": "STABLE"
            },
            "energy": {
                "value": f"R{random.uniform(0.82, 0.88):.2f}/kWh",
                "trend": f"{random.uniform(-3.5, -1.5):.1f}%",
                "status": "ACTIVE"
            }
        }
    }

def feed_data():
    """Send data to Node-RED API every 30 seconds"""
    while True:
        try:
            data = generate_village_data()
            response = requests.post(
                'http://127.0.0.1:1880/village_data',
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 200:
                print(f"✅ Data sent at {datetime.now().strftime('%H:%M:%S')}")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Connection error: {e}")
        
        time.sleep(30)  # Update every 30 seconds

if __name__ == "__main__":
    print("🚀 Imperial Omega Data Feeder Started")
    print("📡 Sending data to Node-RED every 30 seconds")
    print("Press Ctrl+C to stop\n")
    try:
        feed_data()
    except KeyboardInterrupt:
        print("\n📊 Data feeder stopped")
