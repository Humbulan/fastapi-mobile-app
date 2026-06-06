import re

with open('app.py', 'r') as f:
    content = f.read()

# 1. Ensure the JSON routes exist for those buttons
json_routes = """
@app.route('/api/villages/json')
def get_villages_json():
    villages = [
        {"id": 5, "name": "Matsila", "district": "Malamulele", "region": "Limpopo", "pop": 12500},
        {"id": 10, "name": "Bindura Urban", "district": "Bindura", "region": "Mashonaland Central", "pop": 25000}
    ]
    return {"status": "success", "data": villages}

@app.route('/api/keys/json')
def get_keys_json():
    return {"status": "success", "keys": [{"service": "USSD-Gateway", "key": "IMP-778-X"}, {"service": "AI-Engine", "key": "OMEGA-99-Z"}]}
"""

if "/api/villages/json" not in content:
    content = content.replace("app = Flask(__name__)", "app = Flask(__name__)\n" + json_routes)

with open('app.py', 'w') as f:
    f.write(content)

# 2. Update the HTML Template to restore the Yellow Admin Lane
# We are targeting the dashboard.html to add the Admin Tools section
try:
    with open('templates/dashboard.html', 'r') as f:
        html = f.read()
    
    admin_lane_html = """
    <div class="admin-tools-container" style="background: #ffc107; padding: 15px; border-radius: 8px; margin: 20px 0;">
        <h3 style="margin-top:0;">👑 Admin Tools</h3>
        <div style="display: flex; gap: 10px;">
            <a href="/api/villages/json" class="btn btn-light" target="_blank">📂 Villages JSON</a>
            <a href="/api/keys/json" class="btn btn-light" target="_blank">🔑 API Keys JSON</a>
            <button class="btn btn-light" onclick="alert('Add Village Logic Triggered')">➕ Add Village</button>
        </div>
    </div>
    """
    
    if "Admin Tools" not in html:
        # Insert before the "Recent Orders" section
        html = html.replace('<h3>Recent Orders</h3>', admin_lane_html + '<h3>Recent Orders</h3>')
        
    with open('templates/dashboard.html', 'w') as f:
        f.write(html)
    print("✅ Yellow Admin Lane and JSON routes restored.")
except FileNotFoundError:
    print("❌ dashboard.html not found, check template path.")

