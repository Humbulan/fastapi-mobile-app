#!/bin/bash
echo "🚀 IMPERIAL OMEGA STARTUP SEQUENCE"
echo "=================================="

# Start the robust dashboard server on port 8084
cd ~/imperial_network
pkill -f robust_server 2>/dev/null
fuser -k 8084/tcp 2>/dev/null
nohup python3 robust_server.py > robust_server.log 2>&1 &

# Start Node-RED if not running
if ! curl -s http://localhost:1880 >/dev/null 2>&1; then
    cd ~/.node-red
    nohup node-red > node-red.log 2>&1 &
fi

sleep 3
IP=$(ifconfig | grep inet | head -1 | awk '{print $2}' 2>/dev/null || echo "127.0.0.1")
echo "✅ HTML Dashboard: http://$IP:8084"
echo "✅ Node-RED: http://$IP:1880"
echo "✅ Monitor API: http://$IP:8090 (existing service)"
echo "=================================="
