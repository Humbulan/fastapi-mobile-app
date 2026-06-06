#!/bin/bash
# Imperial Alert System - Monitors Port Status and Gold Price

# Configuration
BRIDGE_URL="http://127.0.0.1:8121/imperial-stats"
SMS_ENDPOINT="http://127.0.0.1:8098/send-sms"
EMAIL_ENDPOINT="http://127.0.0.1:8001/send-email"
ALERT_PHONE="0794658481"
ALERT_EMAIL="humbulani@humbu.store"
GOLD_THRESHOLD=5500

# Fetch live data
DATA=$(curl -s $BRIDGE_URL)

# Extract metrics
GOLD=$(echo $DATA | jq -r '.market_prices."Gold (JSE:SSW)"')
STATUS=$(echo $DATA | jq -r '.status')
LIVE_DATA=$(echo $DATA | jq -r '.live_data')

# Check Gold Price Alert
if (( $(echo "$GOLD < $GOLD_THRESHOLD" | bc -l) )); then
    MESSAGE="🚨 IMPERIAL ALERT: Gold price dropped to R$GOLD (below threshold R$GOLD_THRESHOLD)"
    echo "$MESSAGE"
    curl -X POST $SMS_ENDPOINT -H "Content-Type: application/json" -d "{\"phone\":\"$ALERT_PHONE\",\"message\":\"$MESSAGE\"}"
    curl -X POST $EMAIL_ENDPOINT -H "Content-Type: application/json" -d "{\"email\":\"$ALERT_EMAIL\",\"subject\":\"Gold Price Alert\",\"body\":\"$MESSAGE\"}"
fi

# Check for offline ports
OFFLINE_PORTS=$(echo "$LIVE_DATA" | grep -c "🔴 OFFLINE")
if [ "$OFFLINE_PORTS" -gt 0 ]; then
    OFFLINE_DETAILS=$(echo "$LIVE_DATA" | grep "🔴 OFFLINE")
    MESSAGE="🚨 IMPERIAL ALERT: $OFFLINE_PORTS port(s) offline. Details: $OFFLINE_DETAILS"
    echo "$MESSAGE"
    SHORT_MSG="🚨 $OFFLINE_PORTS port(s) offline. Check dashboard."
    curl -X POST $SMS_ENDPOINT -H "Content-Type: application/json" -d "{\"phone\":\"$ALERT_PHONE\",\"message\":\"$SHORT_MSG\"}"
    curl -X POST $EMAIL_ENDPOINT -H "Content-Type: application/json" -d "{\"email\":\"$ALERT_EMAIL\",\"subject\":\"Port Offline Alert\",\"body\":\"$MESSAGE\"}"
fi

# Heartbeat log
if [ "$OFFLINE_PORTS" -eq 0 ] && (( $(echo "$GOLD >= $GOLD_THRESHOLD" | bc -l) )); then
    echo "✅ Imperial Heartbeat: $(date) - All systems nominal. Gold: R$GOLD"
fi
