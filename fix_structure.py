import sys

with open('app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
skip_mode = False

for line in lines:
    # 1. Clear the 'melted' zone (The broken quotes and misaligned metrics)
    if 'SYSTEM CONTEXT' in line:
        new_lines.append('    # SYSTEM CONTEXT: Dashboard Awareness for AI\n')
        new_lines.append('    passed = sum(1 for v in VILLAGES.values() if v["compliance"] == "passed")\n')
        new_lines.append('    warning = sum(1 for v in VILLAGES.values() if v["compliance"] == "warning")\n')
        new_lines.append('    penalty = sum(1 for v in VILLAGES.values() if v["compliance"] == "penalty")\n')
        new_lines.append('    context = f"""\n')
        new_lines.append('    - Network Value: R{TOTAL_WEALTH:,.2f} (R269.9 Trillion)\n')
        new_lines.append('    - Active Villages: {VILLAGE_COUNT}\n')
        new_lines.append('    - Growth Rate: {GROWTH_RATE}%\n')
        new_lines.append('    - 24h Revenue: R{RECENT_REVENUE:,.2f}\n')
        new_lines.append('    - Compliance: {passed} passed, {warning} warnings, {penalty} penalties\n')
        new_lines.append('    - Port of Beira: 78.9% complete (14.2M/18.0M tons)\n')
        new_lines.append('    - Top Village: Beira (R45,300)\n')
        new_lines.append('    - Critical Village: Ha-Mmbara (safety inspection failed)\n')
        new_lines.append('    """\n')
        skip_mode = True
        continue
    
    # 2. Skip until we hit the try block to avoid duplicates
    if skip_mode:
        if 'try:' in line:
            skip_mode = False
            new_lines.append('    try:\n')
        continue
    
    # 3. Fix the HTML Template assignment (Line 290+)
    if 'HTML_TEMPLATE =' in line and '"""' not in line:
        new_lines.append('HTML_TEMPLATE = """\n')
        continue

    new_lines.append(line)

with open('app.py', 'w') as f:
    f.writelines(new_lines)
