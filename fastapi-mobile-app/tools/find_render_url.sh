#!/bin/bash

echo "🔍 FINDING YOUR RENDER DEPLOYMENT"
echo "=================================="

# Common Render URL patterns
POSSIBLE_URLS=(
    "https://fastapi-mobile-app.onrender.com"
    "https://humbulan-fastapi-mobile-app.onrender.com" 
    "https://fastapi-mobile-app-*.onrender.com"
)

echo "📋 Testing common Render URLs..."
for url in "${POSSIBLE_URLS[@]}"; do
    if [[ $url == *"*"* ]]; then
        echo "   Pattern: $url (needs exact name)"
    else
        echo -n "   Testing $url: "
        if curl -s --max-time 5 "$url/health" > /dev/null; then
            echo "✅ LIVE!"
            echo $url > ~/.render_url
            echo "🎯 Found your Render app: $url"
            break
        else
            echo "❌ OFFLINE or wrong URL"
        fi
    fi
done

echo ""
echo "💡 If no URLs worked, check:"
echo "   1. Your Render.com dashboard"
echo "   2. GitHub repo settings -> Deployments"
echo "   3. Look for 'View deployment' in README.md"
