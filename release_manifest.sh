#!/bin/bash
# Release a held manifest

MANIFEST="$1"
if [ -z "$MANIFEST" ]; then
    echo "❌ Usage: ./release_manifest.sh \"Carrier, tons, cargo, route\""
    exit 1
fi

COMPLIANCE_FILE=~/imperial_network/compliance/hold_queue.json
RELEASED_FILE=~/imperial_network/compliance/released.log
PENDING_FILE=~/imperial_network/compliance/pending_manifests.txt

# Remove from hold queue
grep -v "$MANIFEST" "$COMPLIANCE_FILE" > "${COMPLIANCE_FILE}.tmp" 2>/dev/null
mv "${COMPLIANCE_FILE}.tmp" "$COMPLIANCE_FILE" 2>/dev/null

# Remove from pending manifests
grep -v "$MANIFEST" "$PENDING_FILE" > "${PENDING_FILE}.tmp" 2>/dev/null
mv "${PENDING_FILE}.tmp" "$PENDING_FILE" 2>/dev/null

# Log release
echo "$(date +%Y-%m-%d_%H:%M:%S) | RELEASED | $MANIFEST" >> "$RELEASED_FILE"

echo "✅ Manifest released: $MANIFEST"
echo "   Removed from compliance queue"
