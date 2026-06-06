#!/bin/bash

# Colors for terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}📱 MOBILE BUSINESS DASHBOARD${NC}"
echo -e "${CYAN}=============================${NC}"
echo -e "Refreshing every 5 seconds... (Press Ctrl+C to stop)"
echo ""

while true; do
    # Clear screen and show header
    clear
    echo -e "${CYAN}📱 MOBILE BUSINESS DASHBOARD${NC}"
    echo -e "${CYAN}=============================${NC}"
    echo -e "Last updated: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    # Get dashboard data
    RESPONSE=$(curl -s http://localhost:8001/dashboard)
    
    if [ $? -eq 0 ] && [ ! -z "$RESPONSE" ]; then
        # Use Python for reliable JSON parsing and calculations
        python3 -c "
import json, sys
from datetime import datetime

try:
    data = json.loads('''$RESPONSE''')
    dash = data['dashboard']
    quick = data['quick_stats']
    
    # Format values
    revenue = f\"\${dash['total_revenue']:,.2f}\"
    customers = dash['active_customers']
    transactions = dash['today_transactions']
    pending = dash['pending_orders']
    conversion = f\"{dash['conversion_rate'] * 100:.1f}%\"
    status = dash['business_status']
    target = f\"{quick['target_progress']}%\"
    sessions = quick['active_sessions']
    
    # Color code status
    status_color = '\033[1;32m' if status == 'LIVE' else '\033[1;31m'
    
    print(f\"💰  {'Revenue:':<20} {revenue}\")
    print(f\"👥  {'Customers:':<20} {customers}\")
    print(f\"🛒  {'Transactions Today:':<20} {transactions}\")
    print(f\"📦  {'Pending Orders:':<20} {pending}\")
    print(f\"🎯  {'Conversion Rate:':<20} {conversion}\")
    print(f\"🚀  {'Status:':<20} {status_color}{status}\033[0m\")
    print()
    print(f\"📈 {'QUICK STATS':^30}\")
    print(f\"   {'Target Progress:':<18} {target}\")
    print(f\"   {'Active Sessions:':<18} {sessions}\")
    
except Exception as e:
    print(f\"Error: {str(e)}\")
    print(\"Raw response:\")
    print('''$RESPONSE''')
"
        
    else
        echo -e "${RED}❌ Could not connect to API server${NC}"
        echo "   Make sure your FastAPI app is running on port 8001"
        echo "   Command: uvicorn main_mobile:app --host 127.0.0.1 --port 8001 --reload"
    fi
    
    echo ""
    echo -e "${YELLOW}🔄 Refreshing in 5 seconds...${NC}"
    sleep 5
done
