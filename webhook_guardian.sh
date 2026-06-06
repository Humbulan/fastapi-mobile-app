#!/bin/bash
# Imperial Webhook Guardian v2.0 - Response Based
ALERT_FILE=~/imperial_network/imperial_alerts.log
DASHBOARD_SCRIPT=~/imperial_network/update_stealth_ui.sh

check_service() {
    local PORT=$1
    # Check if the port responds to a request
    if curl -s --connect-timeout 2 http://localhost:$PORT > /dev/null; then
        return 0 # Online
    else
        return 1 # Offline
    fi
}

# 1. Check Ukuvuselela Webhook (8117)
if check_service 8117; then
    [ -f /tmp/webhook_was_down ] && rm /tmp/webhook_was_down
else
    if [ ! -f /tmp/webhook_was_down ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') 🚨 CRITICAL - Webhook (8117) unresponsive!" >> "$ALERT_FILE"
        touch /tmp/webhook_was_down
    fi
fi

# 2. Check Regional Ports
for PORT in 8110 8111 9003; do
    if check_service $PORT; then
        [ -f /tmp/port_${PORT}_down ] && rm /tmp/port_${PORT}_down
    else
        if [ ! -f /tmp/port_${PORT}_down ]; then
            echo "$(date '+%Y-%m-%d %H:%M:%S') ⚠️ WARNING - Regional link $PORT timed out" >> "$ALERT_FILE"
            touch /tmp/port_${PORT}_down
        fi
    fi
done

# Update Dashboard
$DASHBOARD_SCRIPT
