#!/bin/bash

echo "🚀 DUAL API MANAGEMENT CONSOLE"
echo "==============================="
echo ""

# Local Simple API
echo "📱 LOCAL SIMPLE API (fastapi-clean)"
echo "------------------------------------"
if curl -s http://localhost:8001/health > /dev/null; then
    echo "✅ Status: RUNNING on port 8001"
    echo "📍 Purpose: Mobile business metrics"
    echo "🎯 Use for: Quick development, testing"
    echo "🔗 URLs:"
    echo "   - http://localhost:8001"
    echo "   - http://localhost:8001/docs"
else
    echo "❌ Status: OFFLINE"
    echo "💡 Start: uvicorn main_mobile:app --reload"
fi

echo ""
echo "🌐 RENDER AI APP (fastapi-mobile-app)"
echo "--------------------------------------"
RENDER_URL=$(cat ~/.render_url 2>/dev/null || echo "UNKNOWN")

if [[ "$RENDER_URL" != "UNKNOWN" ]]; then
    echo -n "🔍 Testing $RENDER_URL: "
    if curl -s --max-time 10 "$RENDER_URL/health" > /dev/null; then
        echo "✅ LIVE"
        echo "📍 Purpose: AI-powered automation"
        echo "🎯 Use for: Production, AI features"
        echo "🔗 URLs:"
        echo "   - $RENDER_URL"
        echo "   - $RENDER_URL/docs"
    else
        echo "❌ OFFLINE (might be sleeping)"
        echo "💡 Free tier: Spins down after inactivity"
    fi
else
    echo "❓ Status: URL UNKNOWN"
    echo "💡 Find your URL at: https://render.com/dashboard"
fi

echo ""
echo "🎯 RECOMMENDED USAGE:"
echo "   Local API → Development & testing"
echo "   Render API → Production & AI features"
echo ""
echo "🔧 MANAGEMENT:"
echo "   ./manage_deployments.sh  - Status overview"
echo "   ./test_both_apis.sh      - Test endpoints"
echo "   git status               - Check changes"
