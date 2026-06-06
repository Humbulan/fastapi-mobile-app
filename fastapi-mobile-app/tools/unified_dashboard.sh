#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 UNIFIED API MANAGEMENT DASHBOARD${NC}"
echo -e "${BLUE}===================================${NC}"
echo ""

# Local API Status
echo -e "${GREEN}📱 LOCAL BUSINESS API${NC}"
echo -e "${GREEN}---------------------${NC}"
LOCAL_DATA=$(curl -s http://localhost:8001/dashboard 2>/dev/null)
if [ $? -eq 0 ]; then
    echo -e "✅ Status: ${GREEN}OPERATIONAL${NC}"
    revenue=$(echo "$LOCAL_DATA" | grep -o '"total_revenue":[0-9]*[.]?[0-9]*' | cut -d: -f2)
    customers=$(echo "$LOCAL_DATA" | grep -o '"active_customers":[0-9]*' | cut -d: -f2)
    echo -e "   💰 Revenue: \$${revenue}"
    echo -e "   👥 Customers: ${customers}"
    echo -e "   🔗 ${BLUE}http://localhost:8001/docs${NC}"
else
    echo -e "❌ Status: ${RED}OFFLINE${NC}"
fi

echo ""

# Render API Status
echo -e "${YELLOW}🌐 RENDER AI APPLICATION${NC}"
echo -e "${YELLOW}------------------------${NC}"
RENDER_URL="https://fastapi-mobile-app.onrender.com"
RENDER_HEALTH=$(curl -s --max-time 10 "$RENDER_URL/health" 2>/dev/null)
if [ $? -eq 0 ]; then
    echo -e "✅ Status: ${GREEN}OPERATIONAL${NC}"
    echo -e "   🤖 AI-Powered Features"
    echo -e "   🐳 Docker Container"
    echo -e "   📊 Business Intelligence"
    echo -e "   🔗 ${BLUE}$RENDER_URL/docs${NC}"
else
    echo -e "🟡 Status: ${YELLOW}SLEEPING or OFFLINE${NC}"
    echo -e "   💡 Free tier: May take 30-60s to wake up"
fi

echo ""
echo -e "${BLUE}🎯 QUICK ACCESS LINKS:${NC}"
echo -e "   Local Docs:    ${BLUE}termux-open-url http://localhost:8001/docs${NC}"
echo -e "   Render Docs:   ${BLUE}termux-open-url $RENDER_URL/docs${NC}"
echo -e "   Render Dashboard: ${BLUE}termux-open-url https://render.com/dashboard${NC}"

echo ""
echo -e "${BLUE}🔧 MANAGEMENT COMMANDS:${NC}"
echo -e "   Test Local:    ${YELLOW}curl http://localhost:8001/dashboard${NC}"
echo -e "   Test Render:   ${YELLOW}curl $RENDER_URL/health${NC}"
echo -e "   View Logs:     ${YELLOW}./enhanced_dashboard.sh${NC}"
