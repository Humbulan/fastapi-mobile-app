with open('app.py', 'r') as f:
    content = f.read()

# 1. Define the global data objects
global_logic = """
@app.context_processor
def inject_global_data():
    user_obj = type('User', (), {'username': 'Humbulani', 'is_authenticated': True})
    stats_data = {'active_users': 261, 'total_revenue': 94000000, 'system_health': 99.9}
    predictions_data = {'revenue': 45600.00, 'orders': 245, 'growth': 15}
    return dict(current_user=user_obj, user=user_obj, stats=stats_data, predictions=predictions_data)
"""

# 2. Inject this logic right after the 'app = Flask' definition
if 'app = Flask(__name__)' in content and '@app.context_processor' not in content:
    content = content.replace('app = Flask(__name__)', 'app = Flask(__name__)\n' + global_logic)

# 3. Clean up the manual render_template calls to be simpler
content = content.replace(", current_user=None, user=type('User', (), {'username': 'Humbulani'})", "")
content = content.replace(", user=type('User', (), {'username': 'Humbulani'})", "")

with open('app.py', 'w') as f:
    f.write(content)

print("✅ Global Context Active. All variables defined for all templates.")
