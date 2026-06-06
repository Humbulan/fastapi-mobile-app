with open('app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
skip_mode = False

for i, line in enumerate(lines):
    # 1. Fix the index function to point correctly
    if 'def index():' in line:
        if i > 0 and '@app.route' not in lines[i-1]:
            new_lines.append("@app.route('/')\n")
        new_lines.append(line)
        continue

    # 2. Find and REWRITE the dashboard function to be clean
    if 'def dashboard():' in line:
        new_lines.append("@app.route('/dashboard')\n")
        new_lines.append("def dashboard():\n")
        new_lines.append("    return render_template_string(HTML_TEMPLATE)\n")
        skip_mode = True
        continue
    
    # Skip lines until the next route to clear out the "old" dashboard junk
    if skip_mode:
        if '@app.route' in line and '/dashboard' not in line:
            skip_mode = False
        else:
            continue

    new_lines.append(line)

with open('app.py', 'w') as f:
    f.writelines(new_lines)
print("✅ Routing Unlocked. Imperial Dashboard Ready.")
