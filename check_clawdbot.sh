#!/bin/bash
echo "🦞 Clawdbot Gateway Status"
echo "=========================="
if pgrep -f clawdbot > /dev/null; then
    echo "✅ Clawdbot: RUNNING (PID: $(pgrep -f clawdbot))"
    echo "📊 Port 18789: $(ss -tln | grep 18789 >/dev/null && echo "LISTENING" || echo "NOT LISTENING")"
    echo "🌐 Public URL: https://imperial.humbu.store/clawdbot/"
    curl -I https://imperial.humbu.store/clawdbot/ 2>/dev/null | head -n1
else
    echo "❌ Clawdbot: NOT RUNNING"
fi
