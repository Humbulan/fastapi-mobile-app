with open('app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    # Inject the Login Logic at the top of the routes
    if 'app = Flask(__name__)' in line:
        new_lines.append("\n@app.route('/login', methods=['GET', 'POST'])\n")
        new_lines.append("def login():\n")
        new_lines.append("    # This connects to your professional login.html\n")
        new_lines.append("    return render_template('login.html')\n")

with open('app.py', 'w') as f:
    f.writelines(new_lines)

print("✅ Security Gateway Restored. Cloudflare Tunnel can now verify the path.")
