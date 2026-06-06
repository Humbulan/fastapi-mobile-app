#!/bin/bash

RENDER_URL="https://fastapi-mobile-app.onrender.com"
echo "🎯 MONITORING BUSINESS API DEPLOYMENT"
echo "====================================="
echo "Target: $RENDER_URL"
echo ""

for attempt in {1..12}; do
    echo "🔄 Attempt $attempt/12 - $(date '+%H:%M:%S')"
    
    # Test the root endpoint
    response=$(curl -s --max-time 15 "$RENDER_URL/" || echo "CURL_ERROR")
    
    if [[ "$response" == *"Connected Business API"* ]]; then
        echo ""
        echo "🎉 🎉 🎉 SUCCESS! BUSINESS API IS LIVE! 🎉 🎉 🎉"
        echo ""
        
        # Test all endpoints
        endpoints=("/" "/health" "/dashboard" "/customers" "/analytics")
        for endpoint in "${endpoints[@]}"; do
            echo -n "🔍 Testing $endpoint: "
            status_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$RENDER_URL$endpoint")
            if [ "$status_code" = "200" ]; then
                echo "✅ WORKING (HTTP $status_code)"
            else
                echo "❌ FAILED (HTTP $status_code)"
            fi
        done
        
        echo ""
        echo "🚀 CONNECTED BUSINESS API v7.0.0 DEPLOYED SUCCESSFULLY!"
        break
        
    elif [[ "$response" == *"<!DOCTYPE html>"* ]]; then
        echo "⏳ Web app still running... (override in progress)"
    elif [[ "$response" == *"CURL_ERROR"* ]]; then
        echo "⏳ Service starting... (attempt $attempt/12)"
    else
        echo "⏳ Deployment in progress... (attempt $attempt/12)"
    fi
    
    sleep 30
done

echo ""
echo "📊 FINAL STATUS:"
curl -s --max-time 10 "$RENDER_URL/health" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print('✅ ' + data.get('service', 'Unknown'))
    print('📦 Version: ' + data.get('version', 'Unknown'))
    print('🕒 Status: ' + data.get('status', 'Unknown'))
    print('⏰ ' + data.get('timestamp', 'Unknown'))
except Exception as e:
    print('❌ Service not responding properly')
    print('💡 Deployment might still be in progress')
"
