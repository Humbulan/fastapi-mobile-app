#!/bin/bash
echo "🏛️ Starting Imperial Omega Dashboard Stack"

# Start Node-RED in background
cd ~/.node-red
node-red &
NODERED_PID=$!
echo "✅ Node-RED started (PID: $NODERED_PID)"

# Wait for Node-RED to initialize
sleep 5

# Start data feeder in background
cd ~/imperial_network
python3 data_feeder.py &
FEEDER_PID=$!
echo "✅ Data feeder started (PID: $FEEDER_PID)"

echo ""
echo "📊 Dashboard URLs:"
echo "   Main UI: http://localhost:1880/ui"
echo "   Editor: http://localhost:1880"
echo ""
echo "To stop all services: kill $NODERED_PID $FEEDER_PID"
echo "View logs: tail -f ~/.node-red/.node-red.log"
