#!/bin/bash
DATE=$(date '+%H:%M:%S')
TOTAL_M=$(wc -l < ~/imperial_network/alerts.log 2>/dev/null || echo "0")
CRIT_M=$(grep -c "CRITICAL" ~/imperial_network/alerts.log 2>/dev/null || echo "0")
WEBHOOK_STATUS=$(lsof -i:8117 >/dev/null && echo "<span style='color:#0f0'>🟢 ACTIVE</span>" || echo "<span style='color:#f00'>🔴 DOWN</span>")
ALERTS=$(tail -n 5 ~/imperial_network/imperial_alerts.log 2>/dev/null || echo "No active alerts")

cat > ~/imperial_network/power_dashboard/index.html << HTML
<!DOCTYPE html>
<html>
<head>
    <title>IMPERIAL COMMAND - WEALTH LOCK</title>
    <style>
        body { background: #000; color: #0f0; font-family: monospace; padding: 20px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        .card { border: 1px solid #050; padding: 15px; background: #010; }
        .alert-card { border: 2px solid #f00; background: #200; color: #f88; }
        h1 { text-align: center; border-bottom: 2px solid #0f0; }
        pre { font-size: 11px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>🌌 IMPERIAL OMEGA COMMAND - $DATE</h1>
    <div class="grid">
        <div class="card">
            <h3>💰 FINANCIAL STATUS</h3>
            <p>Portfolio: R 11,345,774.22</p>
            <p>Valuation: R 1,806,166,092.14</p>
        </div>
        <div class="card">
            <h3>🔗 WEBHOOK (8117)</h3>
            <p>Ukuvuselela: $WEBHOOK_STATUS</p>
        </div>
    </div>

    <div class="card alert-card" style="margin-top: 20px;">
        <h3>🚨 SYSTEM ALERTS (CRITICAL)</h3>
        <pre>$ALERTS</pre>
    </div>

    <div class="card" style="margin-top: 15px;">
        <h3>🚚 LOG FEED</h3>
        <pre>$(tail -n 5 ~/imperial_network/alerts.log)</pre>
    </div>
</body>
</html>
HTML
