import json
from aiohttp import web

# Gauteng Metrics Data
gauteng_score = {"status": "healthy", "gauteng": {"previous": 6.9, "current": 7.8, "target": 8.5}}

async def handle_health(request):
    return web.Response(text=json.dumps(gauteng_score), content_type='application/json')

async def handle_callback(request):
    try:
        data = await request.json()
        with open('flash_rewards.log', 'a') as f:
            f.write(json.dumps(data) + '\n')
        return web.Response(text=json.dumps({'status': 'received'}), content_type='application/json')
    except Exception as e:
        return web.Response(text=json.dumps({'status': 'error', 'message': str(e)}), status=400)

app = web.Application()
app.router.add_get('/health', handle_health)
app.router.add_post('/api/v1/callback', handle_callback)

if __name__ == "__main__":
    web.run_app(app, port=8117)
