import csv
import time
import os
from datetime import datetime

# Path to the record file
CSV_FILE = os.path.expanduser("~/imperial_network/wealth_history.csv")

def log_valuation():
    # Imperial Truth Data
    valuation = 269905078380.45
    gold_price = 84735.00
    lithium_surge = 29.7
    villages = 43
    
    # Check if file exists to write header
    file_exists = os.path.isfile(CSV_FILE)
    
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Valuation (ZAR)", "Gold Price", "Lithium %", "Villages"])
        
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            f"{valuation:.2f}",
            f"{gold_price:.2f}",
            f"{lithium_surge}%",
            villages
        ])
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Wealth Lock Snapshot Saved.")

if __name__ == "__main__":
    print("💰 Wealth Lock Logger: Monitoring R500B Trajectory...")
    while True:
        log_valuation()
        # Wait for 3600 seconds (1 Hour)
        time.sleep(3600)
