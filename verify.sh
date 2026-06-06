#!/bin/bash
echo "🏛️ IMPERIAL OMEGA VERIFICATION"
echo "=============================="
echo ""

# Check Node-RED
echo -n "Node-RED (1880): "
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:1880/

# Check Monitor
echo -n "Monitor API (5001): "
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5001/api/health

echo ""
echo "Latest Metrics:"
curl -s http://localhost:5001/api/metrics | python3 -m json.tool 2>/dev/null

echo ""
echo "Latest Snapshot:"
ls -lth ~/humbu_community_nexus/snapshot_*.html 2>/dev/null | head -1

echo ""
echo "✅ Verification complete"
echo ""
echo "📊 Access points:"
echo "   Dashboard: http://localhost:1880/ui"
echo "   Monitor: http://localhost:5001/"
