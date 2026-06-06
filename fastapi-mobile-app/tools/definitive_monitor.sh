#!/bin/bash

RENDER_URL="https://fastapi-mobile-app.onrender.com"
echo "🎯 DEFINITIVE DEPLOYMENT MONITOR"
echo "================================"

for i in {1..10}; do
    echo ""
    echo "🔄 Check #$i - $(date '+%H:%M:%S')"
    
    # Test the root endpoint
    response=$(curl -s --max-time 10 "$RENDER_URL/")
    
    if echo "$response" | grep -q "Connected Business API"; then
        echo "🎉 SUCCESS: NEW API DEPLOYED!"
        echo ""
        
        # Test all endpoints
        echo "🧪 ENDPOINT TESTS:"
        endpoints=("/health" "/dashboard" "/customers" "/status")
        
        for endpoint in "${endpoints[@]}"; do
            echo -n "🔍 $endpoint: "
            if curl -s --max-time 5 "$RENDER_URL$endpoint" > /dev/null; then
                echo "✅ WORKING"
            else
                echo "❌ FAILED"
            fi
        done
        
        echo ""
        echo "📊 API STATUS:"
        curl -s "$RENDER_URL/health" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(f'Service: {data.get(\"service\", \"Unknown\")}')
    print(f'Version: {data.get(\"version\", \"Unknown\")}')
    print(f'Status: {data.get(\"status\", \"Unknown\")}')
    print(f'Render Connected: {data.get(\"render_connected\", \"Unknown\")}')
except:
    print('Could not parse health endpoint')
"
        
        break
    else
        echo "⏳ Deployment in progress... (attempt $i/10)"
        sleep 30
    fi
done

echo ""
echo "💡 If deployment failed:"
echo "   1. Check https://render.com/dashboard"
echo "   2. Look for build errors"
echo "   3. Ensure only main.py exists in repository"
