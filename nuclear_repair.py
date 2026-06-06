with open('app.py', 'r') as f:
    lines = f.readlines()

clean_lines = []
for line in lines:
    # Strip every single triple-quote line that has been causing these crashes
    if line.strip() in ['"""', 'f"""', 'HTML_TEMPLATE = """']:
        continue
    clean_lines.append(line)

final_lines = []
html_started = False

for line in clean_lines:
    # 1. Re-seal the HTML Template correctly
    if '<!DOCTYPE html>' in line and not html_started:
        final_lines.append('HTML_TEMPLATE = """\n')
        html_started = True
    
    # 2. Skip the duplicate closing tags we added earlier
    if line.strip() in ['</body>', '</html>'] and 'if __name__' not in line:
        continue
        
    final_lines.append(line)

# 3. Add the ONLY closing quote allowed at the very end of the HTML
for i in range(len(final_lines)-1, 0, -1):
    if '</script>' in final_lines[i]:
        final_lines.insert(i + 1, '    </body>\n    </html>\n    """\n')
        break

with open('app.py', 'w') as f:
    f.writelines(final_lines)
print("✅ File Purged and Re-Sealed.")
