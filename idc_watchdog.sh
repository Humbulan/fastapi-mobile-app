#!/bin/bash
# IDC Status Watchdog - Runs every 24 hours
# Logs to: ~/imperial_network/logs/idc_watchdog.log

LOG_DIR="/data/data/com.termux/files/home/imperial_network/logs"
SCRIPT_DIR="/data/data/com.termux/files/home/imperial_network"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] 🏛️ IDC Watchdog Starting..." >> "$LOG_DIR/idc_watchdog.log"

# Check if port 9090 is responding
if curl -s http://localhost:9090 > /dev/null; then
    echo "[$TIMESTAMP] ✅ Port 9090 (IDC_Stealth) is online" >> "$LOG_DIR/idc_watchdog.log"
    
    # Run verification
    if python3 "$SCRIPT_DIR/trace_idc.py" >> "$LOG_DIR/idc_watchdog.log" 2>&1; then
        echo "[$TIMESTAMP] ✅ Verification successful - Status: PERMANENTLY SATISFIED" >> "$LOG_DIR/idc_watchdog.log"
    else
        echo "[$TIMESTAMP] ❌ Verification failed" >> "$LOG_DIR/idc_watchdog.log"
    fi
else
    echo "[$TIMESTAMP] ❌ Port 9090 is not responding" >> "$LOG_DIR/idc_watchdog.log"
fi

echo "[$TIMESTAMP] 🏛️ IDC Watchdog Completed" >> "$LOG_DIR/idc_watchdog.log"
echo "---" >> "$LOG_DIR/idc_watchdog.log"
