#!/bin/bash
# 🏛️ IMPERIAL OMEGA - MASTER STARTUP SCRIPT
# This starts everything: network + tunnel + monitoring

echo "🏛️ IMPERIAL OMEGA STARTUP SEQUENCE"
echo "==================================="
date

# Load environment
set -a
source ~/imperial_network/.env 2>/dev/null
set +a

# Kill any existing processes
echo "🛑 Stopping existing processes..."
pkill -f cloudflared
pkill -f start_imperial_network.sh
pkill -f keep_alive.sh
pkill -f panic_alert.sh
sleep 3

# Clear ports
echo "🔧 Sanitizing ports..."
fuser -k 5173/tcp 8080/tcp 8082/tcp 8083/tcp 8088/tcp 8090/tcp 8117/tcp 2>/dev/null

# Start the Imperial Network
echo "🚀 Launching Imperial Network..."
nohup ~/imperial_network/start_imperial_network.sh > ~/imperial_network/logs/network.log 2>&1 &

# Wait for network to initialize
echo "⏳ Waiting for network to stabilize..."
sleep 10

# Start cloudflared tunnel with auto-reconnect
echo "🌐 Starting Cloudflare Tunnel..."
nohup ~/imperial_network/tunnel_robust.sh > ~/imperial_network/logs/tunnel.log 2>&1 &

# Start monitoring daemon
echo "👁️ Starting monitoring daemon..."
nohup ~/imperial_network/keep_alive.sh > ~/imperial_network/logs/monitor.log 2>&1 &

echo ""
echo "✅ IMPERIAL OMEGA STARTUP COMPLETE"
echo "==================================="
echo "📊 Check status: ~/imperial_network/status.sh"
echo "📝 View logs: tail -f ~/imperial_network/logs/{network,tunnel,monitor}.log"
