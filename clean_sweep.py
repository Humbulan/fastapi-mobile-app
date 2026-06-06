with open('app.py', 'r') as f:
    lines = f.readlines()

final_lines = []
html_content = []
in_html_block = False

for line in lines:
    # 1. Detect the start of the UI
    if '<!DOCTYPE html>' in line:
        in_html_block = True
        final_lines.append('HTML_TEMPLATE = """\n')
    
    # 2. Collect UI lines and ignore stray tags outside the block
    if in_html_block:
        html_content.append(line)
        if '</html>' in line or '</script>' in line:
            # We found a potential end, but keep looking to be sure
            pass
    elif line.strip() not in ['</body>', '</html>', '"""', 'f"""']:
        # Only keep Python code, not stray "debris"
        final_lines.append(line)

# 3. Find the LAST actual UI line and seal it
for line in html_content:
    final_lines.append(line)
    if '</html>' in line or '</script>' in line:
        final_lines.append('"""\n')
        break

with open('app.py', 'w') as f:
    f.writelines(final_lines)
print("✅ Debris Cleared. UI Sealed. Ready for Imperial Launch.")
