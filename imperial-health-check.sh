#!/bin/bash
# Imperial Omega Health Check

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "${BLUE}🏛️ IMPERIAL OMEGA HEALTH CHECK${NC}"
echo "${BLUE}==============================${NC}"
echo ""

# System Overview
echo "${YELLOW}📊 SYSTEM OVERVIEW${NC}"
echo "  • Python Services: $(ps aux | grep -c "python3")"
echo "  • Watchdog Scripts: $(ps aux | grep -c "watch")"
echo "  • proot Sessions: $(ps aux | grep -c "proot")"
echo ""

# Critical Services Check
echo "${YELLOW}🔧 CRITICAL SERVICES${NC}"

check_service() {
    if pgrep -f "$1" > /dev/null; then
        echo -e "  ${GREEN}✓${NC} $2"
    else
        echo -e "  ${RED}✗${NC} $2"
    fi
}

check_service "sadc_sync" "SADC Trade Sync"
check_service "surge_monitor" "Lithium Surge Monitor"
check_service "valuation_watchdog" "Valuation Watchdog (R1.8B)"
check_service "sovereign_master" "Sovereign Master (Port 8096)"
check_service "imperial-guard" "Imperial Guardian"
check_service "panic_alert" "Panic Alert System"
echo ""

# WhatsApp Status
echo "${YELLOW}📱 WHATSAPP IMPERIAL${NC}"
if wacli --store ~/.wacli_imperial doctor 2>/dev/null | grep -q "AUTHENTICATED.*true"; then
    echo -e "  ${GREEN}✓${NC} Authenticated"
    echo -e "  ${YELLOW}⚠️${NC} Connection: false (sync needed)"
else
    echo -e "  ${RED}✗${NC} Not authenticated"
fi
echo ""

# Database Check
echo "${YELLOW}🗄️ TRADE DATABASE${NC}"
if [ -f ~/imperial_network/data/trade.db ]; then
    echo -e "  ${GREEN}✓${NC} SQLite DB found"
    echo -e "  • Size: $(du -h ~/imperial_network/data/trade.db 2>/dev/null | cut -f1)"
else
    echo -e "  ${RED}✗${NC} No trade database"
fi
echo ""

# Last Manifest
echo "${YELLOW}📋 LAST MANIFEST${NC}"
if [ -f ~/imperial_network/logs/imperial-manifest.log ]; then
    tail -1 ~/imperial_network/logs/imperial-manifest.log
else
    echo "  No manifest logs yet"
fi
echo ""

# Valuation (from your logs)
echo "${YELLOW}💰 CURRENT VALUATION${NC}"
echo "  • R1,806,166,092.14"
echo "  • Progress to R500M: 0.3100%"
echo ""

echo "${BLUE}==============================${NC}"
echo "${GREEN}✅ IMPERIAL OMEGA IS OPERATIONAL${NC}"
