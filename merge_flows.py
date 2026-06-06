#!/usr/bin/env python3
import json
import os
import uuid
import sys

# Use Termux paths
home_dir = os.path.expanduser('~')
backup_file = os.path.join(home_dir, 'flows_backup.json')
dashboard_file = os.path.join(home_dir, 'imperial_network/imperial_dashboard_add.json')
merged_file = os.path.join(home_dir, 'imperial_network/merged_flows.json')

# Load existing flows
try:
    with open(backup_file, 'r') as f:
        existing = json.load(f)
    print(f"✅ Loaded existing flows: {len(existing)} nodes")
except FileNotFoundError:
    print("⚠️ No backup file found, starting with empty flow")
    existing = []

# Load new dashboard flows
try:
    with open(dashboard_file, 'r') as f:
        new_flows = json.load(f)
    print(f"✅ Loaded dashboard flows: {len(new_flows)} nodes")
except FileNotFoundError:
    print(f"❌ Dashboard file not found at: {dashboard_file}")
    sys.exit(1)

# Generate new unique IDs for dashboard nodes to avoid conflicts
id_map = {}

for node in new_flows:
    old_id = node.get('id')
    if old_id:
        new_id = str(uuid.uuid4())[:8]
        id_map[old_id] = new_id
        node['id'] = new_id
        print(f"  Mapped {old_id} -> {new_id}")
    
    # Update any references to other nodes
    if 'wires' in node:
        for i, wire_group in enumerate(node['wires']):
            for j, wire_ref in enumerate(wire_group):
                if wire_ref in id_map:
                    node['wires'][i][j] = id_map[wire_ref]

# Append new flows to existing ones
merged = existing + new_flows

# Save merged flows
with open(merged_file, 'w') as f:
    json.dump(merged, f, indent=2)

print(f"\n✅ Flows merged successfully!")
print(f"📊 Total nodes: {len(merged)}")
print(f"💾 Saved to: {merged_file}")
