with open('app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    # We fix the login function to pass a blank user object 
    # so the 'current_user' check in your base.html doesn't crash.
    if 'return render_template(\'login.html\')' in line:
        line = '    return render_template(\'login.html\', current_user=None)\n'
    
    # Do the same for the dashboard
    if 'return render_template(\'admin/villages.html\')' in line:
        line = '    return render_template(\'admin/villages.html\', current_user=None)\n'
        
    new_lines.append(line)

with open('app.py', 'w') as f:
    f.writelines(new_lines)

print("✅ Session context injected. Template crash bypassed.")
