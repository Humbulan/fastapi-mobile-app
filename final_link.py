with open('app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    # Add the missing root route decorator
    if 'def index():' in line:
        new_lines.append("@app.route('/')\n")
    
    # Ensure the dashboard returns the actual template
    if 'def dashboard():' in line:
        new_lines.append("@app.route('/dashboard')\n")
        new_lines.append("def dashboard():\n")
        new_lines.append("    return render_template_string(HTML_TEMPLATE)\n")
        continue
    
    # Skip the old dashboard function lines if they exist to avoid duplicates
    if 'return render_template_string(HTML_TEMPLATE)' in line and '@app.route' not in lines[lines.index(line)-1]:
        continue

    new_lines.append(line)

with open('app.py', 'w') as f:
    f.writelines(new_lines)
print("✅ Routing Linked. Dashboard is live.")
