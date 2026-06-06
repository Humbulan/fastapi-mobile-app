#!/bin/bash
echo "🏛️ IMPERIAL OMEGA DASHBOARD STATUS"
echo "================================"
echo ""

# Check Node-RED
if curl -s http://127.0.0.1:1880/ > /dev/null; then
    echo "✅ Node-RED: Running on port 1880"
    echo "   📊 Dashboard: http://localhost:1880/ui"
    echo "   ✏️ Editor: http://localhost:1880"
else
    echo "❌ Node-RED: Not responding"
fi

# Check API endpoint
echo ""
if curl -s -X POST http://127.0.0.1:1880/village_data -H "Content-Type: application/json" -d '{"test":"ping"}' > /dev/null; then
    echo "✅ API Endpoint: /village_data is active"
else
    echo "❌ API Endpoint: Not responding"
fi

# Check flows.json
echo ""
if [ -f ~/.node-red/flows.json ]; then
    FLOW_COUNT=$(grep -c '"id":' ~/.node-red/flows.json)
    echo "✅ Flows: $FLOW_COUNT nodes loaded"
else
    echo "❌ Flows: flows.json not found"
fi

# Check installed nodes
echo ""
echo "📦 Installed Dashboard Nodes:"
npm list --depth=0 2>/dev/null | grep -E "(dashboard|ui-)" || echo "   No dashboard nodes found"
