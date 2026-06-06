with open('app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
found_dashboard = False

for line in lines:
    if 'def dashboard():' in line:
        found_dashboard = True
    new_lines.append(line)

# If the function is missing (which the 404 confirms), add it at the bottom
if not found_dashboard:
    new_lines.append("\n@app.route('/dashboard')\n")
    new_lines.append("def dashboard():\n")
    # Using 'current_user=None' to prevent the Jinja2 error we saw earlier
    new_lines.append("    return render_template('admin/villages.html', current_user=None)\n")

with open('app.py', 'w') as f:
    f.writelines(new_lines)

print("✅ Dashboard Function Reconstructed. Path to admin/villages.html opened.")
