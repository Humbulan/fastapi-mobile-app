#!/bin/bash

# Get the current API port
PORT=$(cat ~/.api_port 2>/dev/null || echo "8000")
URL="http://localhost:$PORT"

echo "🎯 TESTING API ON PORT $PORT"
echo "============================"

test_endpoint() {
    local endpoint=$1
    local name=$2
    
    echo -n "🔍 $name: "
    response=$(curl -s -w "%{http_code}" "$URL$endpoint")
    http_code="${response: -3}"
    body="${response%???}"
    
    if [ "$http_code" = "200" ]; then
        echo "✅ WORKING"
        # Show a preview
        if [ -n "$body" ] && [ "$body" != "{}" ]; then
            echo "   Preview: $(echo "$body" | head -c 50)..."
        fi
    else
        echo "❌ FAILED (HTTP $http_code)"
    fi
}

test_endpoint "/" "Root endpoint"
test_endpoint "/health" "Health check"
test_endpoint "/dashboard" "Dashboard"
test_endpoint "/customers" "Customers"

echo ""
echo "📚 API Documentation: $URL/docs"
echo "💡 Run './start_api.sh' to restart if needed"
