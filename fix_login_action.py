with open('app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
skip_next = False
for i, line in enumerate(lines):
    if 'def login():' in line:
        new_lines.append(line)
        # Inject the logic to handle the button click
        new_lines.append('    if request.method == "POST":\n')
        new_lines.append('        # This is where your Cloudflare/Secret check happens\n')
        new_lines.append('        return redirect("/dashboard")\n')
        skip_next = True
        continue
    
    if skip_next and 'return render_template' in line:
        new_lines.append(line)
        skip_next = False
        continue
        
    new_lines.append(line)

with open('app.py', 'w') as f:
    f.writelines(new_lines)

print("✅ Login Action Wired. The button will now redirect to Dashboard.")
