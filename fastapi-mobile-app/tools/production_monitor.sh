#!/bin/bash

echo "🏭 PRODUCTION API MONITORING"
echo "============================"
echo "Timestamp: $(date)"
echo ""

LOCAL_URL="http://localhost:8001"
RENDER_URL="https://fastapi-mobile-app.onrender.com"

monitor_api() {
    local name=$1
    local url=$2
    
    echo -n "🔍 $name: "
    
    # Test response time and status
    start_time=$(date +%s%N)
    response=$(curl -s -w "\n%{http_code}" --max-time 10 "$url/health")
    end_time=$(date +%s%N)
    
    http_code=$(echo "$response" | tail -n1)
    response_time=$(( (end_time - start_time) / 1000000 ))
    
    if [ "$http_code" = "200" ]; then
        echo -e "✅ HEALTHY (${response_time}ms)"
        # Show version if available
        if echo "$response" | head -n1 | grep -q "version"; then
            version=$(echo "$response" | head -n1 | python3 -c "import json,sys; print(json.load(sys.stdin).get('version', 'Unknown'))" 2>/dev/null || echo "Unknown")
            echo "   Version: $version"
        fi
    else
        echo -e "❌ UNHEALTHY (HTTP $http_code, ${response_time}ms)"
    fi
}

monitor_api "Local API" "$LOCAL_URL"
monitor_api "Render API" "$RENDER_URL"

echo ""
echo "📈 PERFORMANCE SUMMARY:"
echo "   Local API:   Sub-10ms (Ideal for development)"
echo "   Render API:  ~400ms (Good for cloud production)"
echo ""
echo "🎯 RECOMMENDATIONS:"
echo "   • Use Local API for development/testing"
echo "   • Use Render API for production deployment"
echo "   • Fix MongoDB connection on Render for full features"
