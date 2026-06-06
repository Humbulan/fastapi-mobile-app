#!/bin/bash

echo "🔗 TESTING API CONNECTIONS"
echo "==========================="

CONNECTED_URL="http://localhost:8002"

echo ""
echo "🔍 Testing Connected API Status:"
curl -s "$CONNECTED_URL/connected/status" | python3 -c "
import json, sys
data = json.load(sys.stdin)
status = data['connection_status']
print(f'✅ Connected API: HEALTHY')
print(f'📱 Local API: {status[\"local_api\"]}')
print(f'🌐 Render API: {status[\"render_api\"]}')
"

echo ""
echo "📊 Testing Connected Dashboard:"
curl -s "$CONNECTED_URL/connected/dashboard" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'🔧 Source: {data[\"source\"]}')
if 'local_data' in data:
    local = data['local_data']
    print(f'💰 Revenue: \${local[\"total_revenue\"]}')
    print(f'👥 Customers: {local[\"active_customers\"]}')
if 'ai_enhancements' in data:
    print(f'🤖 AI Enhancements: AVAILABLE')
else:
    print(f'🤖 AI Enhancements: LOCAL ONLY')
"

echo ""
echo "🤖 Testing AI Insights:"
curl -s "$CONNECTED_URL/connected/ai/insights" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(f'✅ AI Insights: WORKING')
    insights = data.get('insights', {})
    if 'revenue_prediction' in insights:
        print(f'   📈 {insights[\"revenue_prediction\"]}')
    if 'customer_growth' in insights:
        print(f'   👥 {insights[\"customer_growth\"]}')
except:
    print('❌ AI Insights: UNAVAILABLE')
"

echo ""
echo "🎯 Connection Summary:"
echo "   Port 8001: Local Business API (Standalone)"
echo "   Port 8002: Connected API (Bridge to Render)"
echo "   Render: AI-Powered Backend"
