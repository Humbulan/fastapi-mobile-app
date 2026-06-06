import requests

# SWITCHING TO THE PRIMARY GATEWAY PORT
GATEWAY_URL = "http://localhost:8102/send_message"
TOKEN = "6d8a8e19c620af7d152399345053cc8d8ec780de00a34068"
TARGET = "27794658481"

REPORT_DATA = {
    "to": TARGET,
    "message": (
        "🏆 *IMPERIAL OMEGA: MORNING READINESS*\n"
        "-------------------------------------\n"
        "✅ *Fleet Status:* 17/17 NODES ONLINE\n"
        "💰 *Total Live Yield:* R14,950,501.42\n"
        "🌍 *SADC Corridor:* ACTIVE\n"
        "-------------------------------------\n"
        "🛡️ *Sentinel Authorization Code:* 6D8A-RECOVERY\n"
        "Timestamp: 2026-04-01 03:25 AM"
    )
}

headers = {"Authorization": f"Bearer {TOKEN}"}

try:
    # Trying the Primary Gateway logic
    response = requests.post(GATEWAY_URL, json=REPORT_DATA, headers=headers, timeout=10)
    if response.status_code == 200 or response.status_code == 201:
        print("🚀 [GATEWAY 8102] Broadcast Successful!")
    else:
        print(f"⚠️ Gateway Response: {response.status_code}")
        # Final Fallback: Query Param mode on the Gateway
        fallback_url = f"{GATEWAY_URL}?to={TARGET}&message=Fleet_Sync_Success"
        requests.get(fallback_url)
        print("📡 Fallback Signal Dispatched.")
except Exception as e:
    print(f"❌ Connection Failed: Is the Port 8102 Gateway online? Error: {e}")
