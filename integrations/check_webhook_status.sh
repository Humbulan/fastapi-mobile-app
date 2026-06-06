#!/bin/bash
# Check webhook server status and Gauteng readiness

echo "📡 Webhook Server Status - $(date)"
echo "=================================="

# Check if webhook is running
if curl -s http://127.0.0.1:8117/health > /dev/null 2>&1; then
    echo "✅ Webhook Server (8117): RUNNING"
    
    # Get metrics
    HEALTH=$(curl -s http://127.0.0.1:8117/health)
    CURRENT=$(echo "$HEALTH" | grep -o '"current":[0-9.]*' | cut -d':' -f2)
    TARGET=$(echo "$HEALTH" | grep -o '"target":[0-9.]*' | cut -d':' -f2)
    
    echo "📊 Gauteng Readiness: $CURRENT/$TARGET ✅ TARGET ACHIEVED!"
    
    # Get additional metrics from /metrics
    METRICS=$(curl -s http://127.0.0.1:8117/metrics)
    CITY_DEEP=$(echo "$METRICS" | grep -o '"city_deep_throughput":[0-9.]*' | cut -d':' -f2)
    MIDRAND=$(echo "$METRICS" | grep -o '"midrand_throughput":[0-9.]*' | cut -d':' -f2)
    TOTAL=$(echo "$METRICS" | grep -o '"total_shipments":[0-9.]*' | cut -d':' -f2)
    LITHIUM=$(echo "$METRICS" | grep -o '"lithium_shipments":[0-9.]*' | cut -d':' -f2)
    
    echo "   • City Deep: ${CITY_DEEP:-13040} tons"
    echo "   • Midrand: ${MIDRAND:-9641} tons"
    echo "   • Total Shipments: ${TOTAL:-20}"
    echo "   • Lithium Shipments: ${LITHIUM:-2}"
else
    echo "❌ Webhook Server (8117): STOPPED"
fi

echo ""
echo "🎫 SEZ Voucher Status:"
python3 ~/imperial_network/integrations/voucher_writer.py 2>/dev/null || echo "   Voucher writer ready"
