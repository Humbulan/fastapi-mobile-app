with open('app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # Detect dashboard or admin functions
    if ('def dashboard' in line or 'def admin' in line or 'def index' in line) and '(' in line:
        if i > 0 and '@app.route' not in lines[i-1]:
            # Add the route directly above the function it found
            route_name = line.split('def ')[1].split('(')[0].strip()
            new_lines.append(f"@app.route('/{route_name}')\n")
            if route_name == "index":
                new_lines.append("@app.route('/')\n")
    
    new_lines.append(line)

with open('app.py', 'w') as f:
    f.writelines(new_lines)
print("✅ Universal Binder applied. Port 8000 routes forced.")
