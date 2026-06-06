#!/bin/bash
echo "📱 Starting Imperial Omega MoMo Services..."

# Ensure Node-RED is running
if ! curl -s http://localhost:1880/ > /dev/null 2>&1; then
    echo "⚠️ Node-RED not running. Starting..."
    cd ~/.node-red
    node-red > ~/imperial_network/logs/nodered.log 2>&1 &
    sleep 5
fi

# Start stats server
pkill -f momo_stats_server 2>/dev/null
cd ~/imperial_network
python3 momo_stats_server.py > ~/imperial_network/logs/momo_stats_server.log 2>&1 &
echo "✅ MoMo Stats Server running on port 5002"

# Wait for services
sleep 2

# Show status
echo ""
echo "📊 MoMo Services Status:"
echo "   Callback: http://localhost:1880/momo/callback"
echo "   Stats: http://localhost:5002/momo/stats"
echo "   Dashboard: http://localhost:1880/ui"
echo ""

# Show quick stats
curl -s http://localhost:5002/momo/stats 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'💰 Total: R{d[\"total_amount\"]:,.2f} | Txn: {d[\"total_transactions\"]} | Payers: {d[\"unique_payers\"]}')" 2>/dev/null

echo ""
echo "✅ MoMo Gateway Operational"
