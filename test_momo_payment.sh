#!/bin/bash
# Test MoMo Callback Endpoint

echo "📱 Testing MoMo Payment Callback"
echo "================================"

# Generate a random transaction ID
TX_ID=$(uuidgen 2>/dev/null || echo "tx-$(date +%s)-$$")
EXTERNAL_ID=$(echo $RANDOM)

echo "Sending test payment..."

curl -X POST http://localhost:1880/momo/callback \
  -H "Content-Type: application/json" \
  -H "X-Reference-Id: $TX_ID" \
  -d "{
    \"financialTransactionId\": \"$TX_ID\",
    \"externalId\": \"$EXTERNAL_ID\",
    \"amount\": \"$(echo "scale=2; $RANDOM/100" | bc)\",
    \"currency\": \"ZAR\",
    \"payer\": {
      \"partyIdType\": \"MSISDN\",
      \"partyId\": \"2779$(printf "%07d" $RANDOM)\"
    },
    \"status\": \"SUCCESSFUL\"
  }"

echo ""
echo "✅ Test complete - Check dashboard at http://localhost:1880/ui"
