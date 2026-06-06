#!/bin/bash
# Imperial Omega: Trade Velocity Logger
LOG_DIR="$HOME/humbu_community_nexus/logs"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date '+%Y-%m-%d %H:%00:%00')
FILE="$LOG_DIR/trade_velocity_$(date +%Y%m%d).log"

# Pull live stats from Port 5003
STATS=$(curl -s http://localhost:5003/sadc/stats)
VOLUME=$(echo $STATS | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('total_volume', 0))" 2>/dev/null || echo "0")
TXNS=$(echo $STATS | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('total_transactions', 0))" 2>/dev/null || echo "0")

# Append to daily nexus log
echo "[$TIMESTAMP] VOLUME: R$VOLUME | TXNS: $TXNS | STATUS: 🟢 ACTIVE" >> "$FILE"
