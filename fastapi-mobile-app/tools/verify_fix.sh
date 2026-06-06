#!/bin/bash

echo "🔍 VERIFYING DEPLOYMENT FIX"
echo "==========================="

echo ""
echo "📁 Local files check:"
echo "Procfile content: $(cat Procfile)"
if [ -f "main.py" ]; then
    echo "main.py exists: ✅"
    echo "First line: $(head -1 main.py)"
else
    echo "main.py: ❌ MISSING"
fi

echo ""
echo "🌐 Checking Render deployment (waiting 30 seconds)..."
sleep 30

RENDER_URL="https://fastapi-mobile-app.onrender.com"
echo ""
echo "Testing endpoints:"

for endpoint in "/health" "/" "/dashboard" "/customers"; do
    echo -n "🔍 $endpoint: "
    if curl -s --max-time 10 "$RENDER_URL$endpoint" > /dev/null; then
        echo "✅ RESPONDING"
    else
        echo "❌ OFFLINE"
    fi
done

echo ""
echo "📊 Current deployment version:"
curl -s "$RENDER_URL/health" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if 'Connected Business API' in str(data):
        print('🎉 SUCCESS: NEW API DEPLOYED!')
    else:
        print('Current version:', data.get('version', 'Unknown'))
        print('Service:', data.get('service', data.get('message', 'Unknown')))
except:
    print('Could not parse response')
"
