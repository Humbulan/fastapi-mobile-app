#!/bin/bash
echo "👻 Ghost Sentry - Port Monitor"
echo "Monitoring ports 8115 and 11434..."
echo "Press Ctrl+C to stop"
echo ""

while true; do
    for port in 8115 11434; do
        if netstat -tuln 2>/dev/null | grep -q ":$port "; then
            echo "[ALERT] $(date '+%H:%M:%S') - Port $port is ACTIVE!"
            netstat -tulpn 2>/dev/null | grep ":$port "
        fi
    done
    sleep 2
done
