with open('app.py', 'r') as f:
    lines = f.readlines()

# Find where the script ends (usually where the last tag was)
new_lines = []
for line in lines:
    if '</body>' in line or '</html>' in line or 'app.run' in line:
        continue
    new_lines.append(line)

# Add the clean closing and startup
new_lines.append('    </body>\n')
new_lines.append('</html>\n')
new_lines.append('"""\n\n')
new_lines.append('if __name__ == "__main__":\n')
new_lines.append('    print("🚀 Imperial Network 2.0 Launching...")\n')
new_lines.append('    print("📍 Dashboard: http://localhost:8000")\n')
new_lines.append('    app.run(host="0.0.0.0", port=8000, debug=True)\n')

with open('app.py', 'w') as f:
    f.writelines(new_lines)
