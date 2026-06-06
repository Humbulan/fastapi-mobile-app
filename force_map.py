with open('app.py', 'r') as f:
    lines = f.readlines()

new_content = []
# Identify the dashboard block to move it
dashboard_block = [
    "\n@app.route('/dashboard')\n",
    "def dashboard():\n",
    "    return render_template('admin/villages.html', current_user=None)\n"
]

# Clean out any existing (broken) dashboard mentions first
clean_lines = [l for l in lines if 'def dashboard():' not in l and "admin/villages.html" not in l and "@app.route('/dashboard')" not in l]

for line in clean_lines:
    new_content.append(line)
    # Inject the dashboard right at the top under the app definition
    if 'app = Flask(__name__)' in line:
        new_content.extend(dashboard_block)

with open('app.py', 'w') as f:
    f.writelines(new_content)

print("✅ Dashboard Force-Mapped to the top of the stack.")
