with open('app.py', 'r') as f:
    content = f.read()

# Fix the template path to the actual file we found
content = content.replace("render_template('admin/villages.html'", "render_template('admin_villages.html'")

with open('app.py', 'w') as f:
    f.write(content)

print("✅ Target Acquired: admin_villages.html linked.")
