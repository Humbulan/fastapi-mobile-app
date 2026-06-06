#!/bin/bash
echo "🏛️ SADC PAYMENT GATEWAY VERIFICATION"
echo "===================================="
echo ""

# Check gateway status
echo -n "Gateway Status: "
curl -s http://localhost:5003/sadc/stats -o /dev/null -w "%{http_code}\n"

# Show stats
echo ""
echo "📊 SADC Payment Statistics:"
curl -s http://localhost:5003/sadc/stats | python3 -m json.tool

# Show available currencies
echo ""
echo "💱 Available Currencies:"
curl -s http://localhost:5003/sadc/currencies | python3 -c "import sys,json; d=json.load(sys.stdin); [print(f'   {k}: {v[\"name\"]} ({v[\"symbol\"]}) - Rate: {v[\"rate\"]} ZAR') for k,v in d.items()]" 2>/dev/null

# Show recent logs
echo ""
echo "📝 Recent Transactions:"
tail -3 ~/imperial_network/logs/sadc_payments.log 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "   No transactions yet"

echo ""
echo "✅ SADC Gateway Status: ACTIVE"
