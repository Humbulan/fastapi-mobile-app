#!/bin/bash

echo "🔧 DATABASE CONNECTION FIX FOR RENDER APP"
echo "=========================================="
echo ""

RENDER_URL="https://fastapi-mobile-app.onrender.com"

echo "🔍 Current Database Status:"
curl -s "$RENDER_URL/health" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'Status: {data[\"status\"]}')
print(f'Database: {data[\"database\"]}')
print(f'Message: {data[\"database_message\"]}')
print(f'Type: {data[\"database_type\"]}')
print(f'Cluster: {data[\"database_message\"]}')
"

echo ""
echo "🎯 POSSIBLE SOLUTIONS:"
echo "   1. Check MongoDB Atlas connection string"
echo "   2. Verify environment variables on Render"
echo "   3. Check network access in MongoDB Atlas"
echo "   4. Review database authentication"

echo ""
echo "🔧 QUICK FIXES TO TRY:"
echo "   1. Visit Render Dashboard → Environment Variables"
echo "   2. Check MONGODB_URL is set correctly"
echo "   3. Whitelist Render IP in MongoDB Atlas"
echo "   4. Restart the Render service"

echo ""
echo "📝 Render Dashboard: https://render.com/dashboard"
echo "📝 MongoDB Atlas: https://cloud.mongodb.com"
