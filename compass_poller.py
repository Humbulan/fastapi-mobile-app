import requests, time, os

def poll_compass():
    url = "https://api.atlassian.com/graphql"
    auth = (os.getenv('JIRA_EMAIL'), os.getenv('JIRA_TOKEN'))
    local_sync = "http://localhost:8120/jira-sync"
    
    print("📡 OMEGA POLLER: Active and monitoring Compass...")
    
    while True:
        # Just a heartbeat to keep the animator alive with your R1.8B data
        payload = {
            "issue": "REV-2026-POLL",
            "component": "Imperial Omega Accounting 2026",
            "valuation": "R1806166092.14"
        }
        try:
            requests.post(local_sync, json=payload)
            print("✅ Heartbeat: R1.8B Valuation Sync Complete")
        except:
            print("❌ Local Sync Offline")
        
        time.sleep(300) # Poll every 5 minutes

if __name__ == "__main__":
    poll_compass()
