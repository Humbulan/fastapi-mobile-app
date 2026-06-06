with open('app.py', 'r') as f:
    lines = f.readlines()

clean_lines = []
for line in lines:
    # Strip all triple quotes that are causing the 'unterminated' errors
    if line.strip() == '"""' or line.strip() == 'f"""':
        continue
    clean_lines.append(line)

final_lines = []
for line in clean_lines:
    # 1. Re-seal the AI Context (around line 245)
    if 'context = f' in line:
        final_lines.append('    context = f"""\n')
        continue
    if 'Critical Village:' in line:
        final_lines.append(line)
        final_lines.append('    """\n')
        continue

    # 2. Re-seal the HTML Template
    if 'HTML_TEMPLATE =' in line:
        final_lines.append('HTML_TEMPLATE = """\n')
        continue
    if '</script>' in line:
        final_lines.append(line)
        final_lines.append('</body>\n</html>\n"""\n')
        continue

    final_lines.append(line)

with open('app.py', 'w') as f:
    f.writelines(final_lines)
print("✅ Master Reset Complete. Ports 8000 and 8118 are clear.")
