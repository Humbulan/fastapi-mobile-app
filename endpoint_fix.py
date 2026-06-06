with open('app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # 1. Force the login route to exist above the function
    if 'def login():' in line:
        if i > 0 and '@app.route' not in lines[i-1]:
            new_lines.append("@app.route('/login', methods=['GET', 'POST'])\n")
    
    # 2. Change the redirect to a hardcoded string to stop the BuildError
    if 'return redirect(url_for("login"))' in line:
        line = '    return redirect("/login")\n'
    
    # 3. Do the same for dashboard just in case
    if 'return redirect(url_for("dashboard"))' in line:
        line = '    return redirect("/dashboard")\n'

    new_lines.append(line)

with open('app.py', 'w') as f:
    f.writelines(new_lines)
print("✅ Endpoints hardcoded. Redirect loop broken.")
