#!/usr/bin/env python3
"""
Project Ukuvuselela Webhook Listener - Budget 2026
Listens for live government rail manifest data on Port 8117
"""
import asyncio
import json
import os
from datetime import datetime
import sys
from aiohttp import web

# Add imperial_network to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Imperial Stack modules
import intel_alpha_8103 as IntelCollector
import b2b_bulk_8114 as B2BProcessor

# Gauteng readiness tracker
gauteng_score = {
    "previous": 6.9,
    "current": 8.5,
    "target": 8.5,
    "last_update": datetime.now().isoformat(),
    "metrics": {
        "city_deep_throughput": 0,
        "midrand_throughput": 0,
        "kaalfontein_throughput": 0,
        "customs_clearance_rate": 0.92
    }
}

async def handle_rail_manifest(request):
    """Handle incoming rail manifest webhooks from government API"""
    try:
        data = await request.json()
        manifest = data.get('manifest', {})
        
        # Initialize processors
        intel = IntelCollector(8103)
        b2b = B2BProcessor(8114)
        
        # Extract manifest details
        manifest_id = manifest.get('manifest_id')
        commodity = manifest.get('commodity_code', '')
        tonnage = manifest.get('gross_tonnage', 0)
        terminal = manifest.get('origin_terminal', 'unknown')
        
        # Check for lithium (Zim-shock premium)
        if commodity == '2616' or 'lithium' in str(manifest).lower():
            # Apply scarcity premium
            premium = 0.15
            valuation = tonnage * 3250 * (1 + premium)
            
            # Update Intel Alpha
            await intel.update_asset_valuation(
                asset_class="lithium_in_transit",
                premium_multiplier=1.15,
                reason="Zim_export_ban_20260225",
                shipment_id=manifest_id
            )
            
            print(f"🔋 LITHIUM PREMIUM APPLIED: {manifest_id} (+15%)")
        
        # Update terminal throughput for Gauteng score
        if terminal == 'city_deep':
            gauteng_score['metrics']['city_deep_throughput'] += tonnage
        elif terminal == 'midrand':
            gauteng_score['metrics']['midrand_throughput'] += tonnage
        elif terminal == 'kaalfontein':
            gauteng_score['metrics']['kaalfontein_throughput'] += tonnage
        
        # Calculate new Gauteng readiness
        await update_gauteng_score()
        
        # Send to B2B Bulk for automotive corridor tracking
        await b2b.process_bulk_shipment({
            'manifest_id': manifest_id,
            'data': manifest,
            'corridor': 'gauteng_ec',
            'timestamp': datetime.now().isoformat(),
            'intel_enhanced': True
        })
        
        return web.json_response({
            'status': 'processed',
            'manifest_id': manifest_id,
            'gauteng_score': gauteng_score['current']
        })
        
    except Exception as e:
        print(f"Error processing manifest: {e}")
        return web.json_response({'status': 'error', 'message': str(e)}, status=500)

async def update_gauteng_score():
    """Calculate Gauteng readiness score based on real metrics"""
    metrics = gauteng_score['metrics']
    
    # Scoring algorithm
    total_throughput = (
        metrics['city_deep_throughput'] + 
        metrics['midrand_throughput'] + 
        metrics['kaalfontein_throughput']
    )
    
    # Base score 6.9 + throughput factor + customs factor
    throughput_score = min(total_throughput / 10000, 1.2)  # Max 1.2 from throughput
    customs_score = metrics['customs_clearance_rate'] * 0.4  # Max 0.4 from customs
    
    new_score = 6.9 + throughput_score + customs_score
    
    # Cap at target 8.5
    gauteng_score['current'] = min(new_score, 8.5)
    gauteng_score['last_update'] = datetime.now().isoformat()
    
    # If we hit 8.5, log the achievement
    if gauteng_score['current'] >= 8.5:
        print("\n🎯 GAUTENG READINESS TARGET ACHIEVED: 8.5/8.5")
        print("📈 Budget 2026 infrastructure milestone reached!")

async def health_check(request):
    """Health check endpoint"""
    return web.json_response({
        'status': 'online',
        'service': 'ukuvuselela_webhook',
        'gauteng_score': gauteng_score['current'],
        'target': gauteng_score['target']
    })

async def get_metrics(request):
    """Return current metrics"""
    return web.json_response(gauteng_score)

async def start_webhook_server():
    """Start the webhook listener on Port 8117"""
    app = web.Application()
    app.router.add_post('/api/webhooks/rail-manifest', handle_rail_manifest)
    app.router.add_get('/api/health', health_check)
    app.router.add_get('/api/metrics', get_metrics)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8117)
    await site.start()
    
    print(f"\n🚂 Project Ukuvuselela Webhook Listener")
    print(f"========================================")
    print(f"📍 Listening on: http://0.0.0.0:8117")
    print(f"📡 Endpoints:")
    print(f"   POST /api/webhooks/rail-manifest - Receive rail data")
    print(f"   GET  /api/health - Health check")
    print(f"   GET  /api/metrics - Gauteng readiness")
    print(f"========================================")
    print(f"📊 Initial Gauteng Score: {gauteng_score['current']}/8.5")
    print(f"🎯 Target: 8.5")
    print(f"\n✅ Webhook server running. Press Ctrl+C to stop.")
    
    # Keep running
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(start_webhook_server())
    except KeyboardInterrupt:
        print("\n\n👋 Webhook server stopped")
        print(f"📊 Final Gauteng Score: {gauteng_score['current']}/8.5")
