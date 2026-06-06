#!/bin/bash
# Imperial Omega Log Maintenance
LOG_DIR="/data/data/com.termux/files/home/imperial_network"
MAX_SIZE=5242880 # 5MB limit per log

for log in $LOG_DIR/*.log; do
    if [ $(stat -c%s "$log") -gt $MAX_SIZE ]; then
        echo "Rotating $log..."
        mv "$log" "$log.bak"
        touch "$log"
    fi
done
