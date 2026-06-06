#!/bin/bash

echo "📱 BUSINESS DASHBOARD - LIVE TERMINAL VIEW"
echo "==========================================="
echo "Refreshing every 5 seconds... (Ctrl+C to stop)"
echo ""

while true; do
    # Clear screen and show header
    clear
    echo "📱 BUSINESS DASHBOARD - LIVE TERMINAL VIEW"
    echo "==========================================="
    echo "Last updated: $(date '+%H:%M:%S')"
    echo ""
    
    # Get dashboard data
    DATA=$(curl -s http://localhost:8001/dashboard)
    
    if [ $? -eq 0 ]; then
        # Extract and display data using Python for calculations
        python3 -c "
import json, sys, os
try:
    data = json.loads('''$DATA''')
    dash = data['dashboard']
    quick = data['quick_stats']
    
    revenue = dash['total_revenue']
    customers = dash['active_customers']
    transactions = dash['today_transactions']
    pending = dash['pending_orders']
    conversion = dash['conversion_rate'] * 100
    status = dash['business_status']
    target_progress = quick['target_progress']
    active_sessions = quick['active_sessions']
    
    print(f'💰  Revenue:        \${revenue:,.2f}')
    print(f'👥  Customers:      {customers}')
    print(f'🛒  Transactions:   {transactions}')
    print(f'📦  Pending Orders: {pending}')
    print(f'🎯  Conversion:     {conversion:.1f}%')
    print(f'🚀  Status:         {status}')
    print('')
    print('📈 QUICK STATS:')
    print(f'   Daily Target Progress: {target_progress}%')
    print(f'   Active Sessions: {active_sessions}')
    
except Exception as e:
    print('Error parsing data')
"
        
    else
        echo "❌ Could not connect to API server"
        echo "   Make sure your FastAPI app is running:"
        echo "   uvicorn main_mobile:app --host 127.0.0.1 --port 8001 --reload"
    fi
    
    echo ""
    echo "⏳ Refreshing in 5 seconds..."
    sleep 5
done
