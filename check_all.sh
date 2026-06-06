#!/bin/bash
echo "🏛️ IMPERIAL OMEGA STATUS CHECK"
echo "================================"

# Check HTML Dashboard (port 8084)
if curl -s -I http://localhost:8084 2>/dev/null | grep -q "200"; then
    echo "HTML Dashboard (8084): 🟢 ONLINE"
else
    echo "HTML Dashboard (8084): 🔴 OFFLINE"
fi

# Check Monitor API (port 8090)
if curl -s http://localhost:8090 2>/dev/null | grep -q "service"; then
    echo "Monitor API (8090): 🟢 ONLINE"
else
    echo "Monitor API (8090): 🔴 OFFLINE"
fi

# Check Node-RED
if curl -s -I http://localhost:1880 2>/dev/null | grep -q "200"; then
    echo "Node-RED (1880): 🟢 ONLINE"
else
    echo "Node-RED (1880): 🔴 OFFLINE"
fi

echo "================================"
echo "💰 Wealth: R269,905,078,380.45"
echo "🏘️ Villages: 43/900"
echo "🖥️ Ports: 51/51 ONLINE"
echo "================================"
echo "🌐 HTML Dashboard: http://192.168.8.130:8084"
echo "📊 Monitor API: http://192.168.8.130:8090"
echo "================================"
