with open('app.py', 'r') as f:
    lines = f.readlines()

final_lines = []
in_html = False

for line in lines:
    # If we see the CSS or the DOCTYPE and haven't started the string yet, START IT
    if ('<!DOCTYPE html>' in line or 'background: linear-gradient' in line) and not in_html:
        final_lines.append('HTML_TEMPLATE = """\n')
        in_html = True
    
    # Keep the line
    final_lines.append(line)

    # If we see the end of the script, CLOSE IT
    if '</script>' in line and in_html:
        final_lines.append('    </body>\n    </html>\n    """\n')
        in_html = False

with open('app.py', 'w') as f:
    f.writelines(final_lines)
print("✅ CSS Captured. String Sealed.")
