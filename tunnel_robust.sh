#!/bin/bash
# 🔄 IMPERIAL TUNNEL - ROBUST VERSION WITH AUTO-RECONNECT

TUNNEL_ID="d512566a-7849-4442-8e07-97b74eaccc37"
LOG_FILE="/data/data/com.termux/files/home/imperial_network/logs/tunnel_robust.log"
CONFIG_FILE="/data/data/com.termux/files/home/.cloudflared/config.yml"

echo "🚇 IMPERIAL TUNNEL DAEMON STARTED at $(date)" >> $LOG_FILE

while true; do
    echo "🔄 Connecting tunnel at $(date)" >> $LOG_FILE
    
    # Try different protocols in case of connectivity issues
    for PROTOCOL in http2 quic; do
        echo "  Trying protocol: $PROTOCOL" >> $LOG_FILE
        # FIXED: Removed the extra --protocol argument
        cloudflared tunnel --config $CONFIG_FILE run $TUNNEL_ID
        EXIT_CODE=$?
        
        if [ $EXIT_CODE -eq 0 ]; then
            echo "✅ Tunnel exited normally at $(date)" >> $LOG_FILE
            break
        else
            echo "⚠️  Tunnel crashed (code: $EXIT_CODE) at $(date)" >> $LOG_FILE
        fi
        
        sleep 2
    done
    
    # Wait before reconnecting (exponential backoff)
    for WAIT in 5 10 20 30; do
        echo "⏳ Waiting ${WAIT}s before reconnect..." >> $LOG_FILE
        sleep $WAIT
        
        # Check if network is back
        if ping -c 1 8.8.8.8 >/dev/null 2>&1; then
            echo "✅ Network detected, reconnecting now" >> $LOG_FILE
            break 2
        fi
    done
    
    echo "🔄 Reconnecting tunnel at $(date)" >> $LOG_FILE
done
