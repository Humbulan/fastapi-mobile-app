#!/data/data/com.termux/files/usr/bin/bash

# Imperial Cloud Verifier - Reconstructed
TOKEN="a8960193-e8ec-4495-95e0-d4c2b3679739"
DB_URI="mongodb://YOUR_LONG_STRING_HERE"

case "$1" in
    quick)
        echo "📡 Quick-Check: $(date)"
        # Check if Atlas is reachable
        nc -zv node1.mongodb.net 27017 && echo "🟢 CLOUD REACHABLE" || echo "🔴 CLOUD BLOCKED"
        ;;
    verify|full)
        echo "🏛️ FULL IMPERIAL AUDIT: $TOKEN"
        python3 -c "import pymongo; c=pymongo.MongoClient('$DB_URI'); print('✅ Status:', c.admin.command('ping'))"
        ;;
    daily)
        echo "🌅 Morning Sync..."
        python3 ~/humbu_community_nexus/cloud_manager_8095.py --sync
        ;;
    *)
        echo "Usage: $0 {quick|verify|daily|audit|full}"
        ;;
esac
