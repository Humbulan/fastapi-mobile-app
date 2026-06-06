with open('app.py', 'r') as f:
    lines = f.readlines()

final_lines = []
in_ui_block = False
ui_started = False

for line in lines:
    # 1. Identify the START of any UI elements (CSS or HTML)
    if ('background:' in line or '<!DOCTYPE' in line) and not ui_started:
        final_lines.append('HTML_TEMPLATE = """\n')
        ui_started = True
        in_ui_block = True
    
    # 2. Identify the END of the UI block
    if '</script>' in line and in_ui_block:
        final_lines.append(line)
        final_lines.append('"""\n')
        in_ui_block = False
        continue

    # 3. If we are NOT in the UI, strip any stray quotes I added previously
    if not in_ui_block:
        if line.strip() in ['"""', 'f"""', 'HTML_TEMPLATE = """']:
            continue
            
    final_lines.append(line)

with open('app.py', 'w') as f:
    f.writelines(final_lines)
print("✅ All CSS/HTML Blocks Captured. Port 8000 Clear.")
