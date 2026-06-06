#!/bin/bash
mkdir -p ~/imperial_network/logs

case "$1" in
    start)
        echo "🏛️ Starting Imperial Omega Full Stack..."
        
        # Kill everything first
        pkill -f node-red 2>/dev/null
        pkill -f data_feeder.py 2>/dev/null
        pkill -f alert_system.py 2>/dev/null
        pkill -f omega_monitor.py 2>/dev/null
        pkill -f simple_monitor.py 2>/dev/null
pkill -f momo_stats_server 2>/dev/null
pkill -f sadc_payment_gateway 2>/dev/null
        pkill -f monitoring_api.py 2>/dev/null
        sleep 2
        
        # Start Node-RED
        cd ~/.node-red
        node-red > ~/imperial_network/logs/nodered.log 2>&1 &
        echo "✅ Node-RED started"
        
        # Wait for Node-RED
        sleep 5
        
        # Start data feeder
        cd ~/imperial_network
        python3 data_feeder.py > ~/imperial_network/logs/feeder.log 2>&1 &
        echo "✅ Data feeder started"
        
        # Start alert system
        python3 alert_system.py > ~/imperial_network/logs/alerts.log 2>&1 &
        echo "✅ Alert system started"
        
        # Start omega monitor on port 5001
        python3 omega_monitor.py > ~/imperial_network/logs/monitor.log 2>&1 &
        # Start MoMo Stats Server
        # Start SADC Payment Gateway

        cd ~/imperial_network

        python3 sadc_payment_gateway.py > ~/imperial_network/logs/sadc_gateway.log 2>&1 &

        echo "✅ SADC Payment Gateway started on port 5003"
    proot-distro login ubuntu -- /root/restart-omega.sh > /dev/null 2>&1 &


        cd ~/imperial_network

        python3 momo_stats_server.py > ~/imperial_network/logs/momo_stats_server.log 2>&1 &

        echo "✅ MoMo Stats Server started on port 5002"
        # Start SADC Payment Gateway

        cd ~/imperial_network

        python3 sadc_payment_gateway.py > ~/imperial_network/logs/sadc_gateway.log 2>&1 &

        echo "✅ SADC Payment Gateway started on port 5003"
    proot-distro login ubuntu -- /root/restart-omega.sh > /dev/null 2>&1 &


        echo "✅ Monitor started on port 5001"
        
        sleep 2
        
        echo ""
        echo "📊 Imperial Omega is fully operational:"
        echo "   Dashboard: http://localhost:1880/ui"
        echo "   Monitor: http://localhost:5001/"
        echo "   API: http://localhost:5001/api/metrics"
        echo "   Health: http://localhost:5001/api/health"
        ;;
        
    stop)
        echo "🛑 Stopping Imperial Omega Services..."
        pkill -f node-red
        pkill -f data_feeder.py
        pkill -f alert_system.py
        pkill -f omega_monitor.py
        pkill -f simple_monitor.py
pkill -f momo_stats_server 2>/dev/null
pkill -f sadc_payment_gateway 2>/dev/null
        pkill -f monitoring_api.py
        echo "✅ All services stopped"
        ;;
        
    status)
        echo "🏛️ Imperial Omega Status"
        echo "======================="
        
        # Check Node-RED
        if curl -s http://127.0.0.1:1880/ > /dev/null 2>&1; then
            echo "✅ Node-RED: Running"
        else
            echo "❌ Node-RED: Not running"
        fi
        
        # Check Monitor
        if curl -s http://127.0.0.1:5001/api/health > /dev/null 2>&1; then
            echo "✅ Monitor: Running on port 5001"
            METRICS=$(curl -s http://127.0.0.1:5001/api/metrics 2>/dev/null)
            VILLAGES=$(echo "$METRICS" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('villages', '?'))" 2>/dev/null)
            echo "   📊 Villages: $VILLAGES"
        else
            echo "❌ Monitor: Not running"
        fi
        
        # Snapshots
        SNAPSHOTS=$(ls ~/humbu_community_nexus/snapshot_*.html 2>/dev/null | wc -l)
        echo "📸 Snapshots: $SNAPSHOTS"
        
        # Processes
        echo ""
        echo "📋 Processes:"
        ps aux | grep -E "(node-red|data_feeder|omega_monitor)" | grep -v grep | awk '{print "   " $11 " (PID: " $2 ")"}' || echo "   No processes"
        ;;
        
    logs)
        echo "📋 Showing logs (Ctrl+C to exit)"
        tail -f ~/imperial_network/logs/monitor.log
        ;;
        
    *)
        echo "Usage: $0 {start|stop|status|logs}"
        ;;
esac
