with open('app.py', 'r') as f:
    lines = f.readlines()

# Separate the definitions from the routes
defs = []
rest = []

for line in lines:
    if 'Flask(__name__)' in line or 'from flask import' in line or 'LoginManager' in line:
        defs.append(line)
    else:
        rest.append(line)

# Reassemble: Imports and App Definition FIRST, then the Routes
with open('app.py', 'w') as f:
    f.writelines(defs)
    f.writelines(rest)

print("✅ App definition moved to Top. System order restored.")
