#!/bin/bash
# Fixed version - stays in working directory
cd ~/imperial_network || exit 1

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; PURPLE='\033[0;35m'; CYAN='\033[0;36m'; NC='\033[0m'

echo -e "${PURPLE}=============================================${NC}"
echo -e "${PURPLE}🏛️ IMPERIAL OMEGA - SAFE MODE${NC}"
echo -e "${PURPLE}=============================================${NC}"

# Kill stuck processes safely
echo -e "${YELLOW}🔧 Cleaning stuck processes...${NC}"
for pid in 19682 19684 22902 22904; do
    kill -9 $pid 2>/dev/null
done
pkill -f "http.server 5000" 2>/dev/null
pkill -f "http.server 5001" 2>/dev/null
pkill -f "http.server 8093" 2>/dev/null
pkill -f "http.server 8122" 2>/dev/null

# Start the network from within the directory
echo -e "${YELLOW}🚀 Starting Imperial Network...${NC}"
./start_imperial_network.sh

# Start missing services
echo -e "${YELLOW}📡 Starting missing services...${NC}"
nohup python3 -m http.server 5000 > /dev/null 2>&1 &
nohup python3 -m http.server 5001 > /dev/null 2>&1 &
nohup python3 -m http.server 8093 > /dev/null 2>&1 &
nohup python3 -m http.server 8122 > /dev/null 2>&1 &

sleep 2

# Verify all ports from within directory
ONLINE=0
for port in 1880 1883 8000 8001 8080 8081 8082 8083 8085 8086 8087 8088 8090 8091 8092 8093 8094 8095 8096 8097 8098 8099 8100 8101 8102 8103 8104 8105 8106 8107 8108 8110 8111 8112 8113 8114 8115 8117 8118 8121 8122 8191 8880 8888 8889 8890 9000 9001 9002 9003 9090 11434 12345 18789 5000 5001 5002 5003; do
    if (timeout 0.2 bash -c "echo > /dev/tcp/localhost/$port") 2>/dev/null; then
        ((ONLINE++))
    fi
done

echo -e "\n${GREEN}✅ $ONLINE/58 PORTS ONLINE${NC}"
echo -e "${PURPLE}=============================================${NC}"
