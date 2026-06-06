#!/bin/bash

echo "🎯 TESTING UNIFIED BUSINESS API"
echo "================================"

UNIFIED_URL="http://localhost:8000"

echo ""
echo "🔍 System Status:"
curl -s "$UNIFIED_URL/status" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'✅ Unified System: {data[\"unified_system\"]}')
print(f'📱 Local API: {data[\"local_api\"]}')
print(f'🌐 Render API: {data[\"render_api\"]}')
"

echo ""
echo "📊 Business Dashboard:"
curl -s "$UNIFIED_URL/dashboard" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'🔧 Source: {data[\"source\"]}')
dashboard = data.get('dashboard', data.get('business_data', {}))
if dashboard:
    print(f'💰 Revenue: \${dashboard[\"total_revenue\"]}')
    print(f'👥 Customers: {dashboard[\"active_customers\"]}')
    print(f'🛒 Transactions: {dashboard[\"today_transactions\"]}')
"

echo ""
echo "🤖 AI-Enhanced Dashboard:"
curl -s "$UNIFIED_URL/ai/dashboard" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'🔧 Source: {data[\"source\"]}')
print(f'🔗 Connection: {data[\"connection_status\"]}')
if 'ai_enhancements' in data:
    print('✅ AI Enhancements: INCLUDED')
    ai = data['ai_enhancements']
    if 'ai_predictions' in ai:
        pred = ai['ai_predictions']
        print(f'   📈 {pred[\"revenue_forecast\"]}')
        print(f'   📈 {pred[\"growth_trend\"]}')
else:
    print('ℹ️  AI Enhancements: LOCAL ONLY')
"

echo ""
echo "👥 Customer Analytics:"
curl -s "$UNIFIED_URL/customers" | python3 -c "
import json, sys
data = json.load(sys.stdin)
analytics = data['analytics']
print(f'👥 Total Customers: {analytics[\"total_customers\"]}')
print(f'⭐ Satisfaction: {analytics[\"satisfaction_score\"]}')
print(f'🤖 AI Enhanced: {data[\"ai_enhanced\"]}')
if 'ai_recommendations' in analytics:
    print('💡 AI Recommendations:')
    for rec in analytics['ai_recommendations']:
        print(f'   • {rec}')
"

echo ""
echo "🎯 Summary:"
echo "   Single API combining local + Render features"
echo "   Automatic fallback if Render unavailable"
echo "   All business endpoints in one place"
