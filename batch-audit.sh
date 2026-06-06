#!/bin/bash
MANIFEST_FILE=~/imperial_network/manifests.txt

echo "🚀 Starting Fresh Imperial Audit (Tactician 1.5B Mode)..."

if [ ! -f "$MANIFEST_FILE" ]; then
    echo "❌ Error: $MANIFEST_FILE not found."
    exit 1
fi

while IFS= read -r manifest || [ -n "$manifest" ]; do
    [ -z "$manifest" ] && continue
    echo "→ Processing: $manifest"
    ~/imperial_network/auditor.sh "$manifest"
    echo "--- Recovery Phase (5s) ---"
    sleep 5
done < "$MANIFEST_FILE"
