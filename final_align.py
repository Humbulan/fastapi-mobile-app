with open('app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'def index():' in line:
        new_lines.append(line)
        # Give index a body so it's not empty
        new_lines.append('    return redirect("/dashboard")\n\n')
        continue
    
    # Skip any stray dashboard lines we just broke
    if "@app.route('/dashboard')" in line or "def dashboard():" in line or "admin/villages.html" in line:
        continue
        
    new_lines.append(line)

# Now add the dashboard function cleanly at the very end
new_lines.append("\n@app.route('/dashboard')\n")
new_lines.append("def dashboard():\n")
new_lines.append("    return render_template('admin/villages.html')\n")

with open('app.py', 'w') as f:
    f.writelines(new_lines)

print("✅ Indentation aligned. Index linked to Dashboard.")
