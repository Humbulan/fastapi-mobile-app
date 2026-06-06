#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 UNIFIED API MANAGEMENT${NC}"
echo -e "${BLUE}========================${NC}"
echo ""

# Check all services
check_service() {
    local name=$1
    local url=$2
    local port=$3
    
    echo -n "🔍 $name (Port $port): "
    if curl -s "$url/health" > /dev/null; then
        echo -e "${GREEN}✅ RUNNING${NC}"
    else
        echo -e "${RED}❌ OFFLINE${NC}"
    fi
}

check_service "Local Business API" "http://localhost:8001" "8001"
check_service "Connected Bridge API" "http://localhost:8002" "8002"

echo ""
echo -e "${YELLOW}🌐 Render AI API${NC}"
RENDER_URL="https://fastapi-mobile-app.onrender.com"
echo -n "🔍 Render AI API: "
if curl -s --max-time 10 "$RENDER_URL/health" > /dev/null; then
    echo -e "${GREEN}✅ AVAILABLE${NC}"
else
    echo -e "${YELLOW}🟡 SLEEPING${NC}"
fi

echo ""
echo -e "${BLUE}🎯 ACCESS POINTS:${NC}"
echo -e "   Local API:    ${BLUE}http://localhost:8001/docs${NC}"
echo -e "   Connected API: ${BLUE}http://localhost:8002/docs${NC}"
echo -e "   Render API:   ${BLUE}$RENDER_URL/docs${NC}"

echo ""
echo -e "${BLUE}🔧 MANAGEMENT:${NC}"
echo -e "   Test Connection: ${YELLOW}./test_connection.sh${NC}"
echo -e "   Local Dashboard: ${YELLOW}./enhanced_dashboard.sh${NC}"
echo -e "   Start Connected: ${YELLOW}uvicorn main_connected:app --port 8002 --reload${NC}"
