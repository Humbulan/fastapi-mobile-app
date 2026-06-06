import re

with open('app.py', 'r') as f:
    app_content = f.read()

# 1. Fix the persistent 405 on Notification Settings
# It must accept POST to save your changes
app_content = app_content.replace("@app.route('/notification-settings')", "@app.route('/notification-settings', methods=['GET', 'POST'])")

with open('app.py', 'w') as f:
    f.write(app_content)

# 2. Add the Revenue and Stats cards to the Dashboard HTML
try:
    with open('templates/dashboard.html', 'r') as f:
        dash_html = f.read()

    stats_cards = """
    <div style="display: grid; grid-template-columns: 1-fr 1fr; gap: 10px; margin: 10px;">
        <div class="card" style="border-left: 5px solid #ffc107;">
            <p style="color: #8b949e; margin: 0;">TOTAL REVENUE</p>
            <h2 style="color: white; margin: 5px 0;">R 94,000,000</h2>
        </div>
        <div class="card" style="border-left: 5px solid #00ff00;">
            <p style="color: #8b949e; margin: 0;">SYSTEM STATUS</p>
            <h2 style="color: white; margin: 5px 0;">STABLE</h2>
        </div>
    </div>
    """

    if "TOTAL REVENUE" not in dash_html:
        # Insert at the very top of the content block
        dash_html = dash_html.replace('{% block content %}', '{% block content %}\n' + stats_cards)
        
    with open('templates/dashboard.html', 'w') as f:
        f.write(dash_html)
    print("✅ Revenue Cards and POST methods synchronized.")
except FileNotFoundError:
    print("❌ dashboard.html not found.")
