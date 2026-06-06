#!/bin/bash
echo "🏛️ Starting Imperial Omega Dashboard Stack"

# Kill any existing processes
pkill -f "node-red" 2>/dev/null
pkill -f "data_feeder.py" 2>/dev/null
sleep 2

# Start Node-RED in background with logging
cd ~/.node-red
node-red > ~/imperial_network/nodered.log 2>&1 &
NODERED_PID=$!
echo "✅ Node-RED started (PID: $NODERED_PID)"

# Wait for Node-RED to fully initialize
echo "⏳ Waiting for Node-RED to initialize..."
sleep 8

# Check if Node-RED is actually running
if curl -s http://127.0.0.1:1880/ > /dev/null; then
    echo "✅ Node-RED is responsive"
else
    echo "⚠️ Node-RED may still be starting, checking logs..."
    tail -5 ~/imperial_network/nodered.log
fi

# Start data feeder
cd ~/imperial_network
python3 data_feeder.py > ~/imperial_network/feeder.log 2>&1 &
FEEDER_PID=$!
echo "✅ Data feeder started (PID: $FEEDER_PID)"

echo ""
echo "📊 Dashboard URLs:"
echo "   Main UI: http://localhost:1880/ui"
echo "   Editor: http://localhost:1880"
echo ""
echo "📝 Log files:"
echo "   Node-RED: ~/imperial_network/nodered.log"
echo "   Feeder: ~/imperial_network/feeder.log"
echo ""
echo "To stop all services: pkill -f node-red; pkill -f data_feeder.py"
echo "View Node-RED logs: tail -f ~/imperial_network/nodered.log"
