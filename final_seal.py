with open('app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    # Remove any stray body or html tags sitting outside of strings
    if line.strip() in ['</body>', '</html>']:
        continue
    new_lines.append(line)

# Find where the script tags end and put the closing quote there
for i in range(len(new_lines)-1, 0, -1):
    if '</script>' in new_lines[i]:
        new_lines.insert(i + 1, '    </body>\n    </html>\n    """\n')
        break

with open('app.py', 'w') as f:
    f.writelines(new_lines)
print("✅ UI Sealed. Ready for launch.")
