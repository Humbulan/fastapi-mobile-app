#!/bin/bash
# 📊 IMPERIAL NETWORK STATUS

echo "🏛️ IMPERIAL OMEGA NETWORK STATUS"
echo "================================"
date

# Tunnel status
TUNNEL_PIDS=$(pgrep -f cloudflared | wc -l)
if [ "$TUNNEL_PIDS" -gt 0 ]; then
    echo "✅ Tunnel: RUNNING ($TUNNEL_PIDS processes)"
else
    echo "❌ Tunnel: STOPPED"
fi

# Count processes instead of ports
NETWORK_PROCS=$(pgrep -f "node|python|flask|gunicorn" | wc -l)
echo "📡 Services running: ~$NETWORK_PROCS processes"

echo ""
echo "🌐 PUBLIC DOMAINS:"
for domain in humbu.store www.humbu.store imperial.humbu.store files.humbu.store monitor.humbu.store secret.humbu.store api.humbu.store; do
    status=$(curl -s -o /dev/null -w "%{http_code}" https://$domain 2>/dev/null)
    if [ "$status" = "200" ] || [ "$status" = "301" ] || [ "$status" = "302" ] || [ "$status" = "401" ] || [ "$status" = "403" ]; then
        echo "  ✅ https://$domain - $status"
    else
        echo "  ⚠️  https://$domain - $status"
    fi
done

echo ""
echo "💰 IMPERIAL WEALTH:"
echo "  SADC Corridor: R269,896,603,967.90"
echo "  Web Upgrades:  R8,474,412.55"
echo "  TOTAL:         R269,905,078,380.45"

# Uptime
echo ""
echo "⏱️  System uptime: $(uptime | sed 's/.*up \([^,]*\),.*/\1/')"

# Last log entries
echo ""
echo "📝 Recent tunnel logs:"
tail -5 ~/imperial_network/logs/tunnel.log 2>/dev/null | sed 's/^/  /'
