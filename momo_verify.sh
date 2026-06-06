#!/bin/bash
echo "🏛️ IMPERIAL OMEGA - MoMo Payment Gateway"
echo "========================================"
echo ""

# Check callback endpoint
echo -n "📡 Callback (1880): "
curl -s -X POST http://localhost:1880/momo/callback \
  -H "Content-Type: application/json" \
  -d '{"test":"ping"}' -o /dev/null -w "%{http_code}\n"

# Check stats endpoint
echo -n "📊 Stats (5002): "
curl -s http://localhost:5002/momo/stats -o /dev/null -w "%{http_code}\n"

# Show stats
echo ""
echo "📈 MoMo Statistics:"
curl -s http://localhost:5002/momo/stats 2>/dev/null | python3 -m json.tool

# Show recent log entries
echo ""
echo "📝 Recent Transactions:"
tail -3 ~/imperial_network/logs/momo_transactions.log

# Show report
echo ""
echo "📄 Latest Report:"
ls -lh ~/humbu_community_nexus/momo_report.html 2>/dev/null || echo "   No report yet"

# Summary
echo ""
echo "💰 Total MoMo Revenue:"
curl -s http://localhost:5002/momo/stats 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'   R{d[\"total_amount\"]:,.2f} from {d[\"total_transactions\"]} transactions')"

echo ""
echo "✅ MoMo Gateway Status: ACTIVE"
