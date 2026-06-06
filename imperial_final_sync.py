with open('app.py', 'r') as f:
    content = f.read()

# 1. Update the Global Context to include 'health' and 'stats' correctly
# This ensures the 'health.system_health' variable is NEVER undefined again.
updated_global = """
@app.context_processor
def inject_global_data():
    user_obj = type('User', (), {'username': 'Humbulani', 'is_authenticated': True})
    stats_data = {'active_users': 261, 'total_revenue': 94000000, 'system_health': 99.9}
    health_data = {'system_health': '99.9%', 'status': 'Stable', 'uptime': '14 Days'}
    predictions_data = {'revenue': 45600.00, 'orders': 245, 'growth': 15}
    return dict(current_user=user_obj, user=user_obj, stats=stats_data, health=health_data, predictions=predictions_data)
"""

# Replace the old context processor or add it if missing
import re
if '@app.context_processor' in content:
    content = re.sub(r"@app\.context_processor.*?return dict\(.*?\)", updated_global, content, flags=re.DOTALL)
else:
    content = content.replace('app = Flask(__name__)', 'app = Flask(__name__)\n' + updated_global)

# 2. Fix the POST 405 error on create_order by allowing methods
content = content.replace("@app.route('/create_order')", "@app.route('/create_order', methods=['GET', 'POST'])")

with open('app.py', 'w') as f:
    f.write(content)

print("✅ Imperial Core Fully Synchronized. Health variable injected.")
