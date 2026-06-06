#!/bin/bash
# Monitor connection bursts to critical ports
THRESHOLD=10
PORTS="5173 8080 8118 8002"
ALERT=0
for port in $PORTS; do
    if command -v ss >/dev/null 2>&1; then
        COUNT=$(ss -tn state established "( sport = :$port )" 2>/dev/null | grep -c "^ESTAB")
    else
        COUNT=$(netstat -tn 2>/dev/null | grep -c ":$port .*ESTABLISHED")
    fi
    if [ "$COUNT" -gt "$THRESHOLD" ]; then
        ALERT=1
        echo "$(date): High connections ($COUNT) on port $port" >> ~/intrusion.log
    fi
done
if [ "$ALERT" -eq 1 ]; then
    echo "$(date): Intrusion suspected – triggering lockdown" >> ~/intrusion.log
    /data/data/com.termux/files/home/bin/imperial-agent "lockdown"
fi
