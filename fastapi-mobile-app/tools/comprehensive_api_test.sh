#!/bin/bash

echo "🧪 COMPREHENSIVE API COMPARISON TEST"
echo "===================================="
echo "Testing both deployments side-by-side"
echo ""

LOCAL_URL="http://localhost:8001"
RENDER_URL="https://fastapi-mobile-app.onrender.com"

test_endpoint() {
    local name=$1
    local local_path=$2
    local render_path=$3
    
    echo "🔍 $name:"
    echo -n "   Local:  "
    if curl -s "${LOCAL_URL}${local_path}" > /dev/null; then
        echo "✅ WORKING"
    else
        echo "❌ FAILED"
    fi
    
    echo -n "   Render: "
    if curl -s --max-time 10 "${RENDER_URL}${render_path}" > /dev/null; then
        echo "✅ WORKING"
    else
        echo "❌ FAILED or TIMEOUT"
    fi
    echo ""
}

# Test all endpoints
test_endpoint "Health Check" "/health" "/health"
test_endpoint "Root Endpoint" "/" "/"
test_endpoint "API Documentation" "/docs" "/docs"
test_endpoint "Dashboard Data" "/dashboard" "/dashboard"
test_endpoint "Customer Analytics" "/customers" "/customers"

echo "📊 PERFORMANCE COMPARISON:"
echo -n "   Local API response time: "
time curl -s -o /dev/null -w "%{time_total}s" "$LOCAL_URL/health" 2>/dev/null
echo ""

echo -n "   Render API response time: "
time curl -s -o /dev/null -w "%{time_total}s" --max-time 10 "$RENDER_URL/health" 2>/dev/null
echo ""

echo "🎯 SUMMARY:"
echo "   📱 Local API:    Fast development & testing"
echo "   🌐 Render API:   Production with AI features"
echo "   💡 Use both for different purposes!"
