#!/bin/bash

RENDER_URL="https://fastapi-mobile-app.onrender.com"
echo "🎯 VERIFYING BUSINESS API DEPLOYMENT"
echo "===================================="

for i in {1..8}; do
    echo ""
    echo "🔄 Check #$i - $(date '+%H:%M:%S')"
    
    response=$(curl -s --max-time 10 "$RENDER_URL/")
    
    if echo "$response" | grep -q "Connected Business API"; then
        echo "🎉 SUCCESS: BUSINESS API DEPLOYED!"
        echo ""
        echo "📊 Testing endpoints:"
        
        endpoints=("/health" "/dashboard" "/customers")
        for endpoint in "${endpoints[@]}"; do
            echo -n "🔍 $endpoint: "
            if curl -s --max-time 5 "$RENDER_URL$endpoint" > /dev/null; then
                echo "✅ WORKING"
            else
                echo "❌ FAILED"
            fi
        done
        
        echo ""
        echo "🚀 BUSINESS API IS LIVE!"
        break
    elif echo "$response" | grep -q "<!DOCTYPE html>"; then
        echo "🔄 Web app still running... (attempt $i/8)"
    else
        echo "⏳ Deploying... (attempt $i/8)"
    fi
    
    sleep 30
done

echo ""
echo "💡 Final status:"
curl -s "$RENDER_URL/health" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(f'Service: {data.get(\\\"service\\\", \\\"Unknown\\\")}')
    print(f'Version: {data.get(\\\"version\\\", \\\"Unknown\\\")}')
except:
    print('Still deploying...')
"
