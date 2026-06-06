#!/bin/bash
echo "🏛️ IMPERIAL OMEGA SNAPSHOT ARCHIVE"
echo "================================="
echo ""

# List all snapshots
if [ -d ~/humbu_community_nexus ]; then
    echo "📸 Available Snapshots:"
    ls -lth ~/humbu_community_nexus/snapshot_*.html | head -10
    echo ""
    echo "Total snapshots: $(ls ~/humbu_community_nexus/snapshot_*.html 2>/dev/null | wc -l)"
    echo ""
    
    # Show latest snapshot
    LATEST=$(ls -t ~/humbu_community_nexus/snapshot_*.html 2>/dev/null | head -1)
    if [ -n "$LATEST" ]; then
        echo "📊 Latest Snapshot: $(basename $LATEST)"
        echo "   Created: $(stat -c %y "$LATEST" 2>/dev/null || stat -f %Sm "$LATEST")"
        echo "   Size: $(du -h "$LATEST" | cut -f1)"
    fi
else
    echo "❌ No snapshot archive found"
fi

echo ""
echo "To open latest snapshot in browser:"
echo "  termux-open \"\$HOME/humbu_community_nexus/\$(ls -t \$HOME/humbu_community_nexus/snapshot_*.html | head -1)\""
