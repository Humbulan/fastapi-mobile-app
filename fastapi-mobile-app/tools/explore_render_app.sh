#!/bin/bash

RENDER_URL="https://fastapi-mobile-app.onrender.com"

echo "🔍 EXPLORING RENDER AI APPLICATION"
echo "==================================="
echo "URL: $RENDER_URL"
echo ""

echo "📡 Testing available endpoints..."
echo ""

# Test root endpoint
echo "1. Root endpoint:"
curl -s "$RENDER_URL" | head -2
echo ""

# Test health endpoint  
echo "2. Health check:"
curl -s "$RENDER_URL/health" | head -2
echo ""

# Check if docs are accessible
echo "3. Documentation:"
echo "   Web: $RENDER_URL/docs"
echo "   Alternative: $RENDER_URL/redoc"
echo ""

# Test for common AI endpoints
echo "4. Testing AI features..."
AI_ENDPOINTS=("/ai" "/automation" "/process" "/analyze" "/predict")

for endpoint in "${AI_ENDPOINTS[@]}"; do
    echo -n "   $endpoint: "
    status=$(curl -s -o /dev/null -w "%{http_code}" "$RENDER_URL$endpoint")
    if [ "$status" = "200" ] || [ "$status" = "404" ]; then
        echo "Exists (HTTP $status)"
    else
        echo "Unknown (HTTP $status)"
    fi
done

echo ""
echo "🎯 NEXT STEPS:"
echo "   Visit: $RENDER_URL/docs for full API documentation"
echo "   Check Render logs for detailed application info"
