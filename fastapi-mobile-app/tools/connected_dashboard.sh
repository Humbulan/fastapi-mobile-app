#!/bin/bash

echo "📱 CONNECTED BUSINESS DASHBOARD"
echo "================================"
echo "Refreshing every 5 seconds... (Ctrl+C to stop)"
echo ""

while true; do
    clear
    echo "📱 CONNECTED BUSINESS DASHBOARD"
    echo "================================"
    echo "Last updated: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    # Get dashboard data
    DATA=$(curl -s http://localhost:8000/dashboard)
    STATUS=$(curl -s http://localhost:8000/status)
    
    if [ $? -eq 0 ]; then
        python3 -c "
import json, sys, os

try:
    dash_data = json.loads('''$DATA''')
    status_data = json.loads('''$STATUS''')
    
    dashboard = dash_data['dashboard']
    quick_stats = dash_data['quick_stats']
    render_enhanced = dash_data['render_enhanced']
    render_status = status_data['render_api']
    
    print(f'💰 Revenue:        \${dashboard[\"total_revenue\"]:,.2f}')
    print(f'👥 Customers:      {dashboard[\"active_customers\"]}')
    print(f'🛒 Transactions:   {dashboard[\"today_transactions\"]}')
    print(f'📦 Pending Orders: {dashboard[\"pending_orders\"]}')
    print(f'🎯 Conversion:     {dashboard[\"conversion_rate\"] * 100:.1f}%')
    print(f'🚀 Status:         {dashboard[\"business_status\"]}')
    print('')
    print(f'📈 Quick Stats:')
    print(f'   Target Progress: {quick_stats[\"target_progress\"]}%')
    print(f'   Active Sessions: {quick_stats[\"active_sessions\"]}')
    print('')
    print(f'🌐 Render AI:')
    print(f'   Connected: {render_enhanced}')
    print(f'   Status:    {render_status}')
    
except Exception as e:
    print('Error loading dashboard data')
"
    else
        echo "❌ Could not connect to API"
    fi
    
    echo ""
    echo "🔄 Refreshing in 5 seconds..."
    sleep 5
done
