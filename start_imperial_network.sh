#!/data/data/com.termux/files/usr/bin/bash

echo "🚀 IMPERIAL NETWORK STARTUP SEQUENCE"
echo "====================================="
cd ~/imperial_network

# Create logs directory if it doesn't exist
mkdir -p logs

# Function to check if a port is in use
check_port() {
    if ss -tuln 2>/dev/null | grep -q ":$1 "; then
        return 0
    else
        return 1
    fi
}

# Start all Imperial services
echo "Starting Imperial Network Services..."

# Store Website (8088)

# Imperial Front Page (8090)
if ! check_port 8097; then
    echo '"  👑 Starting Imperial Front Page (8097)..."'
    cd ~/humbu_community_nexus/restored_projects/api-tester-frontend
    nohup python3 -m http.server 8097 --bind 0.0.0.0 > ~/imperial_network/logs/imperial-front.log 2>&1 &
    cd ~/imperial_network
fi
if ! check_port 8088; then
    echo '"  🏪 Starting Store Website (8088)..."'
    cd ~/humbu_community_nexus/restored_projects/humbu-store-website/public
    nohup python3 -m http.server 8088 --bind 0.0.0.0 > ~/imperial_network/logs/store.log 2>&1 &
    cd ~/imperial_network
fi

# Node-RED (1880, 1883)
if ! check_port 1880; then
    echo '"  📡 Starting REAL Node-RED (1880)..."'
    nohup node-red -p 1880 > logs/node-red.log 2>&1 &
fi
if ! check_port 1883; then
    echo '"  📡 Starting Node-RED Proxy (1883)..."'
    nohup python3 ~/imperial_network/node_red_proxy_1883_enhanced.py > logs/node_red_proxy.log 2>&1 &
fi
if ! check_port 1883; then
    echo '"  📡 Starting Node-RED Proxy (1883)..."'
    nohup python3 ~/imperial_network/node_red_proxy_1883_enhanced.py > logs/node_red_proxy.log 2>&1 &
fi

# Core Business (8000, 8001)
if ! check_port 8000; then
    echo '"  💼 Starting Business API (8000)..."'
    nohup python3 app.py > logs/flask.log 2>&1 &
fi
if ! check_port 8001; then
    echo '"  👑 Starting Admin Portal (8001)..."'
    nohup python3 admin_portal_8001_fixed.py > logs/admin_portal.log 2>&1 &
fi

# Proxy Layer (8080, 8081, 8083)
if ! check_port 8080; then
    echo '"  🌐 Starting Proxy Layer (8080)..."'
    nohup python3 proxy_layer_8080.py > logs/proxy_8080.log 2>&1 &
fi
if ! check_port 8081; then
    echo '"  🏢 Starting Enterprise API (8081)..."'
    nohup python3 proxy_8081.py > logs/proxy_8081.log 2>&1 &
fi
if ! check_port 8083; then
    echo '"  🔄 Starting Redundant Node (8083)..."'
    nohup python3 proxy_8083.py > logs/proxy_8083.log 2>&1 &
fi

# Revenue & Vault (8082, 8085, 8086)
if ! check_port 8082; then
    echo '"  💰 Starting Revenue Bridge (8082)..."'
    nohup python3 revenue_bridge.py > logs/revenue_bridge.log 2>&1 &
fi
if ! check_port 8085; then
    echo '"  🔐 Starting Legacy Vault (8085)..."'
    nohup python3 legacy_vault_fixed.py > logs/legacy_vault.log 2>&1 &
fi
if ! check_port 8086; then
    echo '"  📊 Starting Apex Metrics (8086)..."'
    nohup python3 apex_metrics.py > logs/apex_metrics.log 2>&1 &
fi

# Mobile & Portal (8087, 8088)
if ! check_port 8087; then
    echo '"  📱 Starting USSD Portal (8087)..."'
    nohup python3 ussd_fix.py > logs/ussd.log 2>&1 &
fi
if ! check_port 8088; then
    echo '"  🚪 Starting Portal Master (8088)..."'
    cd ~/humbu_community_nexus/restored_projects/humbu-store-website/public && python3 -m http.server 8088 --bind 0.0.0.0 > ~/imperial_network/logs/portal_master.log 2>&1 &
    cd ~/imperial_network
fi

# Monitoring & Dashboard (8090, 8092)
if ! check_port 8097; then
    echo '"  📈 Starting Monitor (8090)..."'
    nohup python3 monitor_8090.py > logs/monitor.log 2>&1 &
fi
if ! check_port 8092; then
    echo '"  🖥️ Starting Beautiful Dashboard UI (8092)..."'
    nohup python3 dashboard_ui_fixed.py > logs/dashboard.log 2>&1 &
fi

# Intel & Cloud (8094, 8095, 8191)
if ! check_port 8095; then
    # Use filebrowser if available
    if [ -f "/data/data/com.termux/files/usr/bin/filebrowser" ]; then
        nohup filebrowser --port 8095 --address 0.0.0.0 --root ~/humbu_community_nexus/ > logs/filebrowser.log 2>&1 &
    else
        nohup python3 cloud_manager_8095.py > logs/cloud_manager.log 2>&1 &
    fi
fi
if ! check_port 8191; then
    echo '"  📁 Starting Intel Files (8191)..."'
    nohup python3 intel_files_8191.py > logs/intel_files.log 2>&1 &
fi

# Sovereign & B2B (8096, 8099)
if ! check_port 8096; then
    echo '"  👑 Starting Sovereign Master (8096)..."'
    nohup python3 sovereign_master_8096.py > logs/sovereign_master.log 2>&1 &
fi
if ! check_port 8099; then
    echo '"  🤝 Starting B2B Hub (8099)..."'
    nohup python3 b2b_hub_8099.py > logs/b2b_hub.log 2>&1 &
fi

# Regional Portals (8100, 8101, 8102)
if ! check_port 8100; then
    echo '"  🏘️ Starting Malamulele Portal (8100)..."'
    nohup python3 malamulele_fix.py > logs/malamulele.log 2>&1 &
fi
if ! check_port 8101; then
    echo '"  📊 Starting BI Hub (8101)..."'
    nohup python3 bi_hub_8101.py > logs/bi_hub.log 2>&1 &
fi
if ! check_port 8102; then
    echo '"  🌆 Starting Urban Gateway (8102)..."'
    nohup python3 urban_gateway_8102.py > logs/urban_gateway.log 2>&1 &
fi

# Intelligence (8103, 8104, 8105)
if ! check_port 8103; then
    echo '"  🧠 Starting Intel Alpha (8103)..."'
    nohup python3 intel_alpha_8103.py > logs/intel_alpha.log 2>&1 &
fi
if ! check_port 8104; then
    echo '"  ⚡ Starting Surge Monitor (8104)..."'
    nohup python3 surge_monitor_8104.py > logs/surge_monitor.log 2>&1 &
fi
if ! check_port 8105; then
    echo '"  🛡️ Starting Sentinel (8105)..."'
    nohup python3 sentinel_8105.py > logs/sentinel.log 2>&1 &
fi

# Relay Network (8110, 8111, 8112)
if ! check_port 8110; then
    echo '"  🔄 Starting Thohoyandou (8110)..."'
    nohup python3 -m http.server 8110 --bind 0.0.0.0 > logs/thohoyandou.log 2>&1 &
fi
if ! check_port 8111; then
    echo '"  🔄 Starting Malamulele Relay (8111)..."'
    nohup python3 malamulele_relay.py > logs/relay.log 2>&1 &
fi
if ! check_port 8112; then
    echo '"  🌍 Starting SADC Sync (8112)..."'
    nohup python3 sadc_sync_enhanced.py > logs/sadc_sync.log 2>&1 &
fi

# Secondary Vaults (8113, 8114, 8115)
if ! check_port 8113; then
    echo '"  🔐 Starting Vault 2 (8113)..."'
    nohup python3 vault_2_8113.py > logs/vault2.log 2>&1 &
fi
if ! check_port 8114; then
    echo '"  📦 Starting B2B Bulk (8114)..."'
    nohup python3 b2b_bulk_8114.py > logs/b2b_bulk.log 2>&1 &
fi
if ! check_port 8115; then
    echo '"  👻 Starting Ghost (8115)..."'
    nohup python3 ghost_8115.py > logs/ghost.log 2>&1 &
fi

# Brain & Core (8888, 8889)
if ! check_port 8888; then
    echo '"  🧠 Starting System Node (8888)..."'
    nohup python3 system_node_8888.py > logs/brain_8888.log 2>&1 &
fi
if ! check_port 8889; then
    echo '"  💾 Starting PDC Core (8889)..."'
    nohup python3 pdc_backup_8889.py > logs/brain_backup_8889.log 2>&1 &
fi

# HA Tunnel (8880)
if ! check_port 8880; then
    echo '"  🚇 Starting HA Tunnel (8880)..."'
    nohup python3 ~/imperial_network/port_8880.py > logs/ha_tunnel.log 2>&1 &
fi

# Cloud & Stealth (9000, 9090)
if ! check_port 9000; then
    echo '"  ☁️ Starting Nextcloud Core (9000)..."'
    nohup python3 nextcloud_core_9000.py > logs/nextcloud.log 2>&1 &
fi

# Community Tasks (9001-9003)
if ! check_port 9001; then
    echo '"  📋 Starting Thohoyandou Survey (9001)..."'
    nohup python3 ~/imperial_network/port_9001.py > logs/port_9001.log 2>&1 &
fi
if ! check_port 9002; then
    echo '"  📋 Starting Malamulele Pipe Repair (9002)..."'
    nohup python3 ~/imperial_network/port_9002.py > logs/port_9002.log 2>&1 &
fi
if ! check_port 9003; then
    echo '"  📋 Starting Crop Monitoring (9003)..."'
    nohup python3 ~/imperial_network/port_9003.py > logs/port_9003.log 2>&1 &
fi

if ! check_port 9090; then
    echo '"  👻 Starting IDC Stealth (9090)..."'
    nohup python3 idc_stealth_9090.py > logs/stealth_9090.log 2>&1 &
fi

# IDC Dividend Sectors (8106-8108)
if ! check_port 8106; then
    echo '"  🌐 Starting IMPERIAL_WEB_UPGRADE (8106)..."'
    nohup python3 ~/imperial_network/port_8106.py > logs/port_8106.log 2>&1 &
fi
if ! check_port 8107; then
    echo '"  🚚 Starting SADC_A_LOGISTICS (8107)..."'
    nohup python3 ~/imperial_network/port_8107.py > logs/port_8107.log 2>&1 &
fi
if ! check_port 8108; then
    echo '"  🏪 Starting SADC_B_RETAIL (8108)..."'
    nohup python3 ~/imperial_network/port_8108.py > logs/port_8108.log 2>&1 &
fi

# AI Engine (11434)
if ! check_port 11434; then
    echo '"  🤖 Starting Ollama AI (11434)..."'
    nohup ollama serve > logs/ollama.log 2>&1 &
fi



echo '  📊 Starting System Stats (8093)...'
  if ! check_port 8093; then
    nohup python3 system_stats_server_simple.py > logs/system_stats.log 2>&1 &
  fi
echo "Waiting for services to initialize..."
sleep 5

# Update database with all online ports
echo "Updating system sectors in database..."
sqlite3 instance/imperial.db <<SQL
UPDATE system_sectors SET status='online', last_seen=CURRENT_TIMESTAMP
WHERE port IN (1880, 1883, 8000, 8001, 8080, 8081, 8082, 8083, 8085, 8086, 8087, 8088, 8090, 8091, 8092, 8093, 8094, 8095, 8096, 8097, 8098, 8099, 8100, 8101, 8102, 8103, 8104, 8105, 8106, 8107, 8108, 8110, 8111, 8112, 8113, 8114, 8115, 8117, 8191, 8880, 8888, 8889, 9000, 9001, 9002, 9003, 9090, 8118, 11434);

SQL

# Count online ports
ONLINE=$(sqlite3 instance/imperial.db "SELECT COUNT(*) FROM system_sectors WHERE status='online';")
TOTAL=$(sqlite3 instance/imperial.db "SELECT COUNT(*) FROM system_sectors;")

echo "====================================="
echo "✅ IMPERIAL NETWORK: $ONLINE/$TOTAL PORTS ONLINE"
echo "====================================="
echo "📊 Run 'dawn-report-truthful' to see full status"
echo "
echo "🌐 ACCESS YOUR NETWORK:"
echo "   • Admin Portal: http://localhost:8001"
echo "   • Beautiful Dashboard: http://localhost:8092"
echo "   • Node-RED Dashboard: http://localhost:1883"
echo "   • System Monitor: http://localhost:8090"
echo "   • Brain Command: http://localhost:8888"
echo "   • Stealth Node: http://localhost:9090"
echo "
echo "👑 CEO: Humbulani Mudau"

# Start Ukuvuselela webhook (port 8117)
if ! pgrep -f ukuvuselela_standalone.py > /dev/null; then
    echo "Starting Ukuvuselela webhook on port 8117..."
    nohup python3 ~/imperial_network/integrations/ukuvuselela_standalone.py > ~/imperial_network/logs/webhook_8117.log 2>&1 &
else
    echo "✅ Ukuvuselela webhook already running"
fi

# Intel & Cloud (8094, 8095, 8191)

# Intelligence (8103, 8104, 8105)
if ! check_port 8103; then
    echo '"  🧠 Starting Intel Alpha (8103)..."'
    nohup python3 intel_alpha_8103.py > logs/intel_alpha.log 2>&1 &
fi
if ! check_port 8104; then
    echo '"  ⚡ Starting Surge Monitor (8104)..."'
    nohup python3 surge_monitor_8104_fixed.py > logs/surge_monitor.log 2>&1 &
fi
if ! check_port 8105; then
    echo '"  🛡️ Starting Sentinel (8105)..."'
    nohup python3 sentinel_8105.py > logs/sentinel.log 2>&1 &
fi

# Voucher System (8098)
if ! check_port 8098; then
    echo '"  🎫 Starting Voucher API (8098)..."'
    nohup python3 voucher_api.py > logs/voucher_api.log 2>&1 &
fi

# Ukuvuselela Webhook (8117)
if ! check_port 8117; then
    echo '"  🔗 Starting Ukuvuselela Webhook (8117)..."'
    nohup python3 ukuvuselela_webhook_8117.py > logs/webhook_8117.log 2>&1 &
fi

# SEWS Bridge (8091)
if ! check_port 8091; then
    echo '"  🌉 Starting SEWS Bridge (8091)..."'
    nohup python3 sews_bridge_8091.py > logs/sews_bridge.log 2>&1 &
fi

# Intel Redirect (8094)
if ! check_port 8094; then
    echo '"  🛰️ Starting Sky Watcher (8094)..."'
    nohup python3 sky_watcher_8094_fixed.py > logs/sky_watcher.log 2>&1 &
fi
