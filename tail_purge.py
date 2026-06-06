with open('app.py', 'r') as f:
    lines = f.readlines()

# 1. Remove ANY line that is just quotes or stray tags from the end
while lines and (lines[-1].strip() in ['"""', 'f"""', '</body>', '</html>', '']):
    lines.pop()

# 2. Add the clean, final closure
lines.append('\n"""\n') # This closes the HTML_TEMPLATE
lines.append('\nif __name__ == "__main__":\n')
lines.append('    print("🚀 Imperial Network 2.0 Launching...")\n')
lines.append('    app.run(host="0.0.0.0", port=8000, debug=True)\n')

with open('app.py', 'w') as f:
    f.writelines(lines)
print("✅ Tail-end purged and re-aligned.")
