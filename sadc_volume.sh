#!/bin/bash
echo "🏛️ SADC CORRIDOR TRADE VOLUME"
echo "============================="

VOLUME=$(curl -s http://localhost:5003/sadc/stats 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"{d.get('total_volume', 0):,.2f}\")" 2>/dev/null || echo "0.00")
TXNS=$(curl -s http://localhost:5003/sadc/stats 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('total_transactions', 0))" 2>/dev/null || echo "0")

echo "💰 Total Trade Volume: R$VOLUME"
echo "📊 Total Transactions: $TXNS"
echo ""
echo "📋 Recent Corridor Activity:"
curl -s http://localhost:5003/sadc/stats 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); [print(f'   • {c}') for c in d.get('active_corridors', [])[:5]]" 2>/dev/null || echo "   No corridors active"
