#!/bin/bash
echo "⚔️ INITIALIZING IMPERIAL OMEGA SYNC..."
echo "====================================="
date

# 1. ONLY kill specific clawdbot processes if they're misbehaving
# DO NOT kill everything else
pkill -f "clawdbot.*--port 18789" 2>/dev/null

# 2. Sync Environment & Identity
echo "🔑 Loading credentials..."
source ~/.bashrc 2>/dev/null
source ~/imperial_network/.env 2>/dev/null
export IMPERIAL_KEY="admin123"
export CLOUDFLARE_API_TOKEN="N0avaGCMgL-iOaTVL9xJuBgY_FcJ01YtSs7bJZBh"
export ZONE_ID="16b85e1c695921a4d56305e4a94438e8"
export OPENCLAW_GATEWAY_TOKEN="6d8a8e19c620af7d152399345053cc8d8ec780de00a34068"

# 3. Check if clawdbot is already running
if pgrep -f "clawdbot.*--port 18789" > /dev/null; then
    echo "✅ Clawdbot already running (PID: $(pgrep -f clawdbot))"
else
    echo "🦞 Starting Clawdbot Gateway on port 18789..."
    nohup clawdbot gateway --port 18789 --allow-unconfigured > ~/imperial_network/logs/clawdbot.log 2>&1 &
    sleep 2
    if pgrep -f clawdbot > /dev/null; then
        echo "  ✅ Clawdbot Gateway started (PID: $(pgrep -f clawdbot))"
    else
        echo "  ❌ Clawdbot Gateway failed to start"
    fi
fi

# 4. Check if tunnel is running, start if not
if ! pgrep -f cloudflared > /dev/null; then
    echo "🌐 Starting Cloudflare Tunnel..."
    nohup ~/imperial_network/tunnel_robust.sh > ~/imperial_network/logs/tunnel.log 2>&1 &
    sleep 3
fi

# 5. Verify clawdbot endpoint
echo ""
echo "🔍 Verifying clawdbot endpoint..."
curl -I http://localhost:18789/ 2>/dev/null | head -n1
echo ""
echo "🌐 Public URL: https://imperial.humbu.store/clawdbot/"

echo ""
echo "✅ IMPERIAL OMEGA SYNC COMPLETE"
echo "====================================="
date
