#!/bin/bash

echo "🎯 TESTING CONNECTED BUSINESS API"
echo "================================"
URL="http://localhost:8000"

echo ""
echo "🔍 Testing All Endpoints:"

endpoints=(
    "/"
    "/health" 
    "/dashboard"
    "/customers"
    "/transactions?limit=3"
    "/revenue?days=3"
    "/products"
    "/status"
)

for endpoint in "${endpoints[@]}"; do
    echo -n "🔍 $endpoint: "
    response=$(curl -s -w "%{http_code}" "$URL$endpoint")
    http_code="${response: -3}"
    
    if [ "$http_code" = "200" ]; then
        echo "✅ WORKING"
        # Show quick preview
        body="${response%???}"
        if [[ $endpoint == "/dashboard" ]]; then
            revenue=$(echo "$body" | grep -o '"total_revenue":[0-9]*[.]?[0-9]*' | cut -d: -f2)
            customers=$(echo "$body" | grep -o '"active_customers":[0-9]*' | cut -d: -f2)
            echo "   💰 Revenue: \$$revenue, 👥 Customers: $customers"
        fi
    else
        echo "❌ FAILED (HTTP $http_code)"
    fi
done

echo ""
echo "🌐 Render Connection Status:"
curl -s "$URL/status" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'📱 Local API: {data[\"local_api\"]}')
print(f'🌐 Render API: {data[\"render_api\"]}')
print(f'🔗 System: {data[\"connected_system\"]}')
"

echo ""
echo "📚 Documentation: $URL/docs"
