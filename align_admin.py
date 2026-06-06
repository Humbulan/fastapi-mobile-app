with open('app.py', 'r') as f:
    content = f.read()

# 1. Clean up the 'double' definitions at the top that are blocking the real ones
import re
content = re.sub(r"@app\.route\('/admin/villages'\)\ndef route_get_villages.*?\n", "", content)

# 2. Re-point the Dashboard to use the MASTER logic
# This ensures it passes the 'stats' variable needed for the "Full" look (Image 112357)
if 'def dashboard():' in content:
    content = content.replace(
        'return render_template(\'dashboard.html\', current_user=None, user=type(\'User\', (), {\'username\': \'Humbulani\'}))',
        'return render_template(\'dashboard.html\', current_user=None, user=type(\'User\', (), {\'username\': \'Humbulani\'}), stats=get_stats())'
    )

# 3. Ensure the API routes are properly linked to their data functions
if 'def get_stats():' in content and "@app.route('/api/admin/stats')" not in content:
    content = content.replace('def get_stats():', "@app.route('/api/admin/stats')\ndef get_stats():")

if 'def get_villages():' in content and "@app.route('/api/admin/villages')" not in content:
    content = content.replace('def get_villages():', "@app.route('/api/admin/villages')\ndef get_villages():")

with open('app.py', 'w') as f:
    f.write(content)

print("✅ Admin Routes Aligned. Conflict removed.")
