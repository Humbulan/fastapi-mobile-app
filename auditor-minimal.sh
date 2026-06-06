#!/bin/bash
# MINIMAL WORKING VERSION

MANIFEST="$1"
if [ -z "$MANIFEST" ]; then
    echo "❌ Error: No manifest provided."
    exit 1
fi

echo "🦞 IMPERIAL AUDITOR - Humbu Wandeme Trading Enterprise"
echo "==================================================="
echo "📋 Manifest: $MANIFEST"
echo ""

# Simple JSON using the exact format that worked
curl -s -X POST http://127.0.0.1:11434/api/generate \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"qwen2.5:1.5b\",
    \"prompt\": \"Verify this manifest: $MANIFEST\",
    \"stream\": false
  }" | jq -r '.response'

echo ""
echo "==================================================="
