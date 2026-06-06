#!/bin/bash
# 👁️ IMPERIAL KEEP-ALIVE MONITOR
# Checks all services every 60 seconds and restarts if needed

LOG_FILE="/data/data/com.termux/files/home/imperial_network/logs/keep_alive.log"

echo "👁️ IMPERIAL KEEP-ALIVE STARTED at $(date)" >> $LOG_FILE

while true; do
    DATE=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Check tunnel
    if ! pgrep -f "cloudflared tunnel run" > /dev/null; then
        echo "$DATE - ⚠️ Tunnel down, restarting..." >> $LOG_FILE
        nohup ~/imperial_network/tunnel_robust.sh > ~/imperial_network/logs/tunnel.log 2>&1 &
    fi
    
    # Check network services (at least 40 ports should be up)
    PORTS_UP=$(netstat -tln | grep -c "0.0.0.0:[0-9]*" || echo "0")
    if [ "$PORTS_UP" -lt 20 ]; then
        echo "$DATE - ⚠️ Only $PORTS_UP ports up, restarting network..." >> $LOG_FILE
        pkill -f start_imperial_network.sh
        sleep 2
        nohup ~/imperial_network/start_imperial_network.sh > ~/imperial_network/logs/network.log 2>&1 &
    fi
    
    # Check internet connectivity
    if ! ping -c 1 8.8.8.8 >/dev/null 2>&1; then
        echo "$DATE - ⚠️ Internet down, waiting..." >> $LOG_FILE
    else
        # Check if domains are accessible
        if ! curl -s -o /dev/null -w "%{http_code}" https://imperial.humbu.store/ | grep -q "200\|301\|302\|401\|403"; then
            echo "$DATE - ⚠️ Domain not accessible, restarting tunnel..." >> $LOG_FILE
            pkill -f cloudflared
            sleep 2
            nohup ~/imperial_network/tunnel_robust.sh > ~/imperial_network/logs/tunnel.log 2>&1 &
        fi
    fi
    
    # Log status every hour
    if [ $(( $(date +%M) % 60 )) -eq 0 ]; then
        PORTS=$(netstat -tln | grep -c "0.0.0.0:[0-9]*")
        echo "$DATE - 📊 STATUS: $PORTS ports, Tunnel: $(pgrep -f cloudflared | wc -l) processes" >> $LOG_FILE
    fi
    
    sleep 60
done
