with open('app.py', 'r') as f:
    lines = f.readlines()

# Find the absolute first and last boundaries
first_ui_index = -1
last_ui_index = -1

for i, line in enumerate(lines):
    if 'background:' in line or '<!DOCTYPE' in line:
        if first_ui_index == -1: first_ui_index = i
    if '</html>' in line or '</script>' in line:
        last_ui_index = i

if first_ui_index != -1 and last_ui_index != -1:
    new_lines = []
    # 1. Keep Python code before the UI
    new_lines.extend(lines[:first_ui_index])
    
    # 2. Start the Master String
    new_lines.append('HTML_TEMPLATE = """\n')
    
    # 3. Add UI content, but STRIP any triple-quotes that might be inside
    for i in range(first_ui_index, last_ui_index + 1):
        clean_line = lines[i].replace('"""', "'''") # Neutralize interior quotes
        new_lines.append(clean_line)
    
    # 4. Close the Master String
    new_lines.append('"""\n')
    
    # 5. Add the rest of the Python code
    new_lines.extend(lines[last_ui_index + 1:])

    with open('app.py', 'w') as f:
        f.writelines(new_lines)
    print("✅ Master UI Block Sealed. No more decimal literal leaks.")
else:
    print("❌ Could not determine UI boundaries.")
