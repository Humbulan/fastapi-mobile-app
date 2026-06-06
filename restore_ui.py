with open('app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    # Inject the UI routes after the index function
    if 'def index():' in line:
        new_lines.append("\n@app.route('/dashboard')\n")
        new_lines.append("def dashboard():\n")
        # This points to your actual professional dashboard file
        new_lines.append("    return render_template('admin/villages.html')\n")

# Fix the index redirect to go to the dashboard since login is missing
with open('app.py', 'w') as f:
    for line in new_lines:
        if 'return redirect("/login")' in line:
            f.write('    return redirect("/dashboard")\n')
        else:
            f.write(line)

print("✅ UI Route Reconnected to admin/villages.html")
