with open('app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # Find the problematic tags
    if line.strip() in ['</body>', '</html>', '"""']:
        # Look at the line BEFORE it to find the correct indentation
        prev_line = lines[i-1]
        indent = len(prev_line) - len(prev_line.lstrip())
        new_lines.append(" " * indent + line.lstrip())
    else:
        new_lines.append(line)

with open('app.py', 'w') as f:
    f.writelines(new_lines)
print("✅ Indentation matched to code block. Ready.")
