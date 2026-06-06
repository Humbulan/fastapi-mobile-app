with open('app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # If we find the dashboard function but it's missing the route, add it
    if 'def dashboard():' in line:
        # Check if the line above is already a route to avoid duplicates
        if i > 0 and '@app.route' not in lines[i-1]:
            new_lines.append("@app.route('/dashboard')\n")
    
    # Ensure the login route exists too
    if 'def login():' in line:
        if i > 0 and '@app.route' not in lines[i-1]:
            new_lines.append("@app.route('/login', methods=['GET', 'POST'])\n")
            
    new_lines.append(line)

with open('app.py', 'w') as f:
    f.writelines(new_lines)
print("✅ Routes re-mapped to your professional templates.")
