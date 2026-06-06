import subprocess
import re
import json
import requests
from datetime import datetime, UTC

# Routed via Microsoft Fabric Real-Time Intelligence ingestion hub
POWER_BI_API_URL = "https://api.powerbi.com/beta/0ebcb09b-8658-41a4-bad7-bf4100aa92ae/datasets/2165b478-4386-4839-b4c0-a61c962637d4/rows?experience=power-bi&key=SIOXFEYZx7ZS5X7EVg6KE8meD05zSSNTWaelqX0WCnmGT3eNavVqiHhuSdjm%2BmkOjuI2KSRMcoBWa%2F0aEwwneQ%3D%3D"

def parse_and_stream():
    print("[*] Running local Dawn Report script to parse infrastructure metrics...")
    
    result = subprocess.run(['/bin/bash', 'dawn_report_enhanced.sh'], capture_output=True, text=True)
    output = result.stdout

    try:
        portfolio_val = float(re.search(r"PORTFOLIO VALUE:\s*R([\d\.]+)", output).group(1))
        progress_val = float(re.search(r"PROGRESS TO R500B:\s*([\d\.]+)%", output).group(1))
        ports_verified = int(re.search(r"STATUS:\s*(\d+)/\d+\s*ports verified", output).group(1))
        
        trade_volume_str = re.search(r"TRADE VOLUME:\s*R([\d,\.]+)", output).group(1)
        trade_volume = float(trade_volume_str.replace(',', ''))
        
        gold_monthly = float(re.search(r"GOLD EXPORTS:.*Monthly:\s*([\d\.]+)M", output, re.DOTALL).group(1))
    except AttributeError as e:
        print(f"[-] Data parsing discrepancy detected against script strings: {e}")
        return

    current_time = datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    payload = [{
        "timestamp": current_time,
        "portfolio_value": portfolio_val,
        "progress_percentage": progress_val,
        "active_ports": ports_verified,
        "sadc_trade_volume": trade_volume,
        "gold_monthly_m": gold_monthly
    }]
    
    print("[*] Generated Data Package:")
    print(json.dumps(payload, indent=2))

    print("[*] Syncing streaming payload directly with Power BI Premium Fabric framework...")
    try:
        response = requests.post(POWER_BI_API_URL, data=json.dumps(payload))
        if response.status_code == 200:
            print("[+] Success! Imperial Workspace state synchronized.")
        else:
            print(f"[-] Service rejected transmission: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[-] Core pipeline delivery network fault: {str(e)}")

if __name__ == "__main__":
    parse_and_stream()
