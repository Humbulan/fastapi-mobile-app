with open('app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    # Re-link the UI to your MASTER dashboard
    if 'def dashboard():' in line:
        if "@app.route('/dashboard')" not in new_lines[-1]:
            new_lines.append("@app.route('/dashboard')\n")
    
    # Re-link the Data API for the villages
    if 'def get_villages():' in line:
        if "@app.route('/api/admin/villages')" not in new_lines[-1]:
            new_lines.append("@app.route('/api/admin/villages')\n")
            
    # Re-link the Stats API
    if 'def get_stats():' in line:
        if "@app.route('/api/admin/stats')" not in new_lines[-1]:
            new_lines.append("@app.route('/api/admin/stats')\n")

    new_lines.append(line)

with open('app.py', 'w') as f:
    f.writelines(new_lines)

print("✅ Original Connections Restored. No new code added.")
