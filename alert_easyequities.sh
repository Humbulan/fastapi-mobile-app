#!/bin/bash
# Imperial Omega: Ticket 3603792 (Sync-Aware Logic)
LOG_FILE="$HOME/imperial_network/logs/easyequities_alerts.log"
STORE="$HOME/.wacli_imperial"
JID="27794658481@s.whatsapp.net"

while true; do
  # Check if log was modified in the last 2 minutes
  if find "$LOG_FILE" -mmin -2 | grep -q "."; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') [DEBUG] Change detected. Pausing sync for alert..." >> ~/imperial_network/logs/ussd_alerts.log
    
    # 1. Briefly pause the sync process to release the lock
    pkill -STOP -f "wacli.*sync"
    sleep 2
    rm -f "$STORE/LOCK" # Force clear if pkill-STOP didn't release it
    
    # 2. Send the alert
    wacli --store "$STORE" send text --to "$JID" --message "🚨 IMPERIAL ALERT: EasyEquities Update (Ticket 3603792). Check your mailbox." &>/dev/null
    
    # 3. Resume the sync process
    pkill -CONT -f "wacli.*sync"
    
    echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] VIP Alert Sent & Sync Resumed" >> ~/imperial_network/logs/ussd_alerts.log
    sleep 300 # Cool down
  else
    sleep 20
  fi
done
