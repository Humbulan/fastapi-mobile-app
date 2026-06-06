#!/bin/bash
# Imperial Omega Snapshot Backup System
# Supports local, remote, and cloud backups

BACKUP_DIR="$HOME/humbu_community_nexus/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/imperial_snapshots_$TIMESTAMP.tar.gz"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Create compressed archive of all snapshots
tar -czf "$BACKUP_FILE" -C "$HOME" humbu_community_nexus/snapshot_*.html 2>/dev/null

if [ $? -eq 0 ] && [ -f "$BACKUP_FILE" ]; then
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "✅ Local backup created: $BACKUP_FILE ($SIZE)"
    
    # Optional: Copy to Termux shared storage for easy access
    if [ -d "$HOME/storage/downloads" ]; then
        cp "$BACKUP_FILE" "$HOME/storage/downloads/"
        echo "   📱 Copied to Downloads folder"
    fi
    
    # Optional: Keep only last 30 backups
    cd "$BACKUP_DIR"
    ls -t imperial_snapshots_*.tar.gz 2>/dev/null | tail -n +31 | xargs -r rm
    echo "   🧹 Cleaned old backups (kept last 30)"
    
    # Record backup in log
    echo "$TIMESTAMP: Backup created ($SIZE)" >> "$BACKUP_DIR/backup_history.log"
else
    echo "❌ No snapshots found to backup"
fi

# Optional: Git backup (if using git)
if command -v git &> /dev/null && [ -d "$HOME/humbu_community_nexus/.git" ]; then
    cd "$HOME/humbu_community_nexus"
    git add snapshot_*.html 2>/dev/null
    git commit -m "Auto-backup: $TIMESTAMP" 2>/dev/null
    echo "   📦 Git commit created"
fi

echo "📊 Backup Summary:"
echo "   - Total snapshots: $(ls -1 $HOME/humbu_community_nexus/snapshot_*.html 2>/dev/null | wc -l)"
echo "   - Backup size: $SIZE"
echo "   - Location: $BACKUP_FILE"
