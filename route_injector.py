with open('app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
injected = False

for line in lines:
    new_lines.append(line)
    # Find the app definition and inject immediately after
    if 'app = Flask(__name__)' in line and not injected:
        new_lines.append("\n@app.route('/dashboard')\n")
        new_lines.append("def dashboard():\n")
        new_lines.append("    return render_template_string(HTML_TEMPLATE)\n\n")
        injected = True

    # Fix the index redirect to not use url_for (avoiding the build error)
    if 'return redirect(url_for("dashboard"))' in line:
        new_lines[-1] = '    return redirect("/dashboard")\n'

with open('app.py', 'w') as f:
    f.writelines(new_lines)
print("✅ Route Injected. Build Error Bypassed.")
