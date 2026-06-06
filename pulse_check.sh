#!/bin/bash
# Imperial Wealth Pulse Check - Refined

# Fetch Live JSON from the Bridge
DATA=$(curl -s http://127.0.0.1:8121/imperial-stats)

# Precise extraction using jq (matching the JSON keys exactly)
GOLD=$(echo $DATA | jq -r '.market_prices."Gold (JSE:SSW)"')
ZAR=$(echo $DATA | jq -r '.market_prices.ZAR_USD')
BASE_VAL="269905078380"

echo "-------------------------------------------------------"
echo "🏛️  IMPERIAL WEALTH PULSE | $(date)"
echo "-------------------------------------------------------"
echo "📍 BASE VALUATION:  R269.9 Billion"
echo "💹 LIVE GOLD (SSW): R$GOLD"
echo "🇿🇦 ZAR/USD RATE:   R$ZAR"

# Simple status check
if [[ "$GOLD" != "null" && "$GOLD" != "N/A" ]]; then
    echo "⚖️  STATUS: Market synchronized. Portfolio is ACTIVE."
else
    echo "⚠️  STATUS: Link established, but market data is pending."
fi
echo "-------------------------------------------------------"
