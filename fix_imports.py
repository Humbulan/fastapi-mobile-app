with open('app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'from flask import' in line:
        # Ensure all necessary tools are imported
        line = "from flask import Flask, render_template, redirect, url_for, request, jsonify\n"
    new_lines.append(line)

with open('app.py', 'w') as f:
    f.writelines(new_lines)

print("✅ Imports Unified. Imperial Engine Ready.")
