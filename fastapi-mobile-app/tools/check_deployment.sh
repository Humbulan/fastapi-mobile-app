#!/bin/bash

echo "🔍 CHECKING RENDER DEPLOYMENT STATUS"
echo "===================================="

RENDER_URL="https://fastapi-mobile-app.onrender.com"

echo ""
echo "⏳ Waiting for Render to deploy (this may take 2-3 minutes)..."
sleep 10

echo ""
echo "🧪 Testing deployed endpoints:"

endpoints=("/health" "/" "/dashboard" "/customers" "/status")

for endpoint in "${endpoints[@]}"; do
    echo -n "🔍 $endpoint: "
    response=$(curl -s --max-time 10 -w "%{http_code}" "$RENDER_URL$endpoint")
    http_code="${response: -3}"
    
    if [ "$http_code" = "200" ]; then
        echo "✅ DEPLOYED & WORKING"
        # Show quick preview for dashboard
        if [ "$endpoint" = "/dashboard" ]; then
            body="${response%???}"
            echo "   Preview: $(echo "$body" | head -c 50)..."
        fi
    elif [ "$http_code" = "000" ]; then
        echo "🔄 STILL DEPLOYING (timeout)"
    else
        echo "❌ HTTP $http_code"
    fi
done

echo ""
echo "🌐 Deployment Summary:"
curl -s "$RENDER_URL/health" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(f'✅ Service: {data.get(\"service\", \"Unknown\")}')
    print(f'✅ Version: {data.get(\"version\", \"Unknown\")}')
    print(f'✅ Status: {data.get(\"status\", \"Unknown\")}')
    print(f'✅ Render Connected: {data.get(\"render_connected\", \"Unknown\")}')
except Exception as e:
    print('❌ Deployment in progress...')
    print(f'   Error: {str(e)}')
"

echo ""
echo "📊 If deployment is complete, test with:"
echo "   python api_client.py  # Using local version"
echo "   Or update api_client.py to use: $RENDER_URL"
