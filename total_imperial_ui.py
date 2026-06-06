import re

with open('app.py', 'r') as f:
    app_content = f.read()

# 1. Fix the 405 error for Notification Settings
if "methods=['GET', 'POST']" not in app_content:
    app_content = app_content.replace("@app.route('/notification-settings')", "@app.route('/notification-settings', methods=['GET', 'POST'])")

with open('app.py', 'w') as f:
    f.write(app_content)

# 2. Re-write base.html with the Correct CSS and Bottom Navigation Icons
base_html_premium = """
<!DOCTYPE html>
<html>
<head>
    <title>Imperial Network 2.0</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body { background: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding-bottom: 80px; }
        .bottom-nav { position: fixed; bottom: 0; width: 100%; background: #161b22; display: flex; justify-content: space-around; padding: 15px 0; border-top: 2px solid #ffc107; }
        .bottom-nav a { color: #8b949e; text-decoration: none; font-size: 20px; text-align: center; }
        .bottom-nav a.active { color: #ffc107; }
        .admin-lane { background: #ffc107; color: black; padding: 15px; border-radius: 0 0 15px 15px; margin-bottom: 20px; font-weight: bold; }
        .card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px; margin: 10px; }
        .btn-imperial { background: #ffc107; color: black; border: none; padding: 10px; border-radius: 5px; font-weight: bold; width: 100%; }
    </style>
</head>
<body>
    <div class="admin-lane">
        <span>👑 CEO: Humbulani Mudau</span>
        <span style="float: right;">v2.0.4-Omega</span>
    </div>
    
    <div class="container">
        {% block content %}{% endblock %}
    </div>

    <div class="bottom-nav">
        <a href="/dashboard"><i class="fas fa-home"></i><br><span style="font-size:10px;">HOME</span></a>
        <a href="/my_payments"><i class="fas fa-wallet"></i><br><span style="font-size:10px;">PAY</span></a>
        <a href="/my_orders"><i class="fas fa-box"></i><br><span style="font-size:10px;">ORDERS</span></a>
        <a href="/ai/dashboard"><i class="fas fa-robot"></i><br><span style="font-size:10px;">AI</span></a>
        <a href="/notification-settings"><i class="fas fa-cog"></i><br><span style="font-size:10px;">SYSTEM</span></a>
    </div>
</body>
</html>
"""

with open('templates/base.html', 'w') as f:
    f.write(base_html_premium)

print("✅ Imperial Premium UI applied. FontAwesome Icons loaded.")
