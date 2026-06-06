#!/bin/bash
echo "🔓 IMPERIAL TUNNEL WAKE UP COMMAND"
export GODEBUG=netdns=go
pkill -f cloudflared
sleep 2
nohup cloudflared tunnel --config /data/data/com.termux/files/home/.cloudflared/config.yml \
  --edge-ip-version 4 \
  --protocol http2 \
  run d512566a-7849-4442-8e07-97b74eaccc37 > /data/data/com.termux/files/home/imperial_network/logs/tunnel.log 2>&1 &
sleep 5
echo "✅ TUNNEL ACTIVATED"
echo "Check with: grep \"Registered\" ~/imperial_network/logs/tunnel.log"
