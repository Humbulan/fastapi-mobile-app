with open('app.py', 'r') as f:
    content = f.read()

# 1. Kill the fake template string entirely
import re
content = re.sub(r"HTML_TEMPLATE = '''.*?'''", "", content, flags=re.DOTALL)

# 2. Remove the hardcoded dashboard function I injected
content = re.sub(r"@app.route\('/dashboard'\)\s+def dashboard\(\):.*?return render_template_string\(HTML_TEMPLATE\)", "", content, flags=re.DOTALL)

# 3. Ensure index redirects to YOUR login, not my broken dashboard
content = content.replace('return redirect("/dashboard")', 'return redirect(url_for("login"))')

with open('app.py', 'w') as f:
    f.write(content)

print("✅ Garbage purged. System redirected to Login Gateway.")
