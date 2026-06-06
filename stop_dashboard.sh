#!/bin/bash
echo "🛑 Stopping Imperial Omega Dashboard Stack"

# Kill Node-RED processes
pkill -f "node-red" 2>/dev/null && echo "✅ Node-RED stopped" || echo "ℹ️ Node-RED not running"

# Kill data feeder
pkill -f "data_feeder.py" 2>/dev/null && echo "✅ Data feeder stopped" || echo "ℹ️ Data feeder not running"

# Verify ports are free
sleep 2
if ! curl -s http://127.0.0.1:1880/ > /dev/null 2>&1; then
    echo "✅ Port 1880 is free"
else
    echo "⚠️ Port 1880 still in use"
fi

echo "🏛️ Imperial Omega Dashboard stopped"
