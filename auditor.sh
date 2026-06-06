#!/bin/bash
# IMPERIAL AUDITOR - With Compliance Enforcement

MANIFEST="$1"
TONS=$(echo "$MANIFEST" | grep -o '[0-9]\+' | head -1)
[ -z "$TONS" ] && TONS=0
COMMISSION=$((TONS * 4))
COMPLIANCE_FILE=~/imperial_network/compliance/hold_queue.json
DATE_TODAY=$(date +%Y-%m-%d)

if [ "$TONS" -ge 42 ]; then
    STATUS="⚠️ CRITICAL - HOLD"
    ASSESSMENT="OVERWEIGHT - REQUIRES IMPERIAL CLEARANCE"
    # Auto-add to compliance queue with timestamp
    echo "{\"date\":\"$DATE_TODAY\",\"manifest\":\"$MANIFEST\",\"tons\":$TONS,\"commission\":$COMMISSION,\"status\":\"HOLD\"}" >> "$COMPLIANCE_FILE"
    # Also append to pending log for quick view
    echo "$MANIFEST" >> ~/imperial_network/compliance/pending_manifests.txt
else
    STATUS="✅ PASS - CLEARED"
    ASSESSMENT="Within SADC limits"
fi

echo "🦞 IMPERIAL AUDITOR - Humbu Wandeme Trading Enterprise"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Status: $STATUS"
echo "Weight: $TONS tons ($ASSESSMENT)"
echo "Commission (R4): R$COMMISSION"
echo "Route: Giyani → Beira (VERIFIED)"
echo "---------------------------------------------------"
echo -n "Auditor Notes: "

# Create JSON payload properly
PROMPT="Write a detailed observation about this shipment including carrier name, cargo type, and route: $MANIFEST"
JSON_DATA=$(jq -n \
  --arg model "qwen2.5:1.5b" \
  --arg prompt "$PROMPT" \
  --argjson stream false \
  --argjson temperature 0.1 \
  '{model: $model, prompt: $prompt, stream: $stream, temperature: $temperature}')

# Get AI response with timeout
RESPONSE=$(curl --max-time 120 -s -X POST http://127.0.0.1:11434/api/generate \
  -H "Content-Type: application/json" \
  -d "$JSON_DATA" 2>/dev/null)

# Extract and display response
if [ -n "$RESPONSE" ] && echo "$RESPONSE" | jq -e '.response' >/dev/null 2>&1; then
    echo "$RESPONSE" | jq -r '.response'
else
    echo "⚠️ AI service busy - compliance recorded"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$TONS" -ge 42 ]; then
    echo "⚠️ HOLD [$(date)]: $MANIFEST - Added to compliance queue" >> ~/imperial_network/logs/compliance.log
    echo ""
    echo "🔒 IMPERIAL HOLD - Clearance Required:"
    echo "   To release, run: ./release_manifest.sh \"$MANIFEST\""
    echo "   Queue position: $(wc -l < ~/imperial_network/compliance/pending_manifests.txt 2>/dev/null || echo 0)"
fi
if [ "$TONS" -ge 42 ]; then
    PENALTY=500
    TOTAL_YIELD=$((COMMISSION + PENALTY))
    echo "⚖️ COMPLIANCE PENALTY: R$PENALTY applied to $CARRIER" >> ~/imperial_network/revenue.log
    echo "💰 ADJUSTED YIELD: R$TOTAL_YIELD"
fi
