import sqlite3
from datetime import datetime

db_path = 'instance/imperial.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. DEFINE THE FULL 17-VEHICLE FLEET (Bridging the gap)
full_fleet = [
    ('IMP-01', 'Malamulele Plaza', 'Active - CEO Escort'),
    ('IMP-02', 'Masingita Crossing', 'Active - R15M Audit'),
    ('IMP-03', 'Bindura Urban', 'Standby'),
    ('IMP-04', 'Shamva North', 'Maintenance'),
    ('IMP-05', 'Giyani Hub', 'Active'),
    ('IMP-06', 'Thohoyandou Center', 'Active'),
    ('IMP-07', 'Musina Border', 'SADC Corridor'),
    ('IMP-08', 'Beira Port', 'SADC Corridor'),
    ('IMP-09', 'Polokwane Gateway', 'Active'),
    ('IMP-10', 'Pretoria North', 'Gauteng Node'),
    ('IMP-11', 'Sandton Apex', 'Gauteng Node'),
    ('IMP-12', 'Johannesburg South', 'Gauteng Node'),
    ('IMP-13', 'Soweto West', 'Active'),
    ('IMP-14', 'Masingita Crossing', 'Backup'),
    ('IMP-15', 'Mukhomi', 'Patrol'),
    ('IMP-16', 'Gumbani', 'Relay'),
    ('IMP-17', 'Imperial HQ', 'Strategic Reserve')
]

print("🛡️ Purging Stale Node Data...")
cursor.execute("DELETE FROM gauteng_nodes")

print("🚛 Injecting Full 17-Vehicle Fleet...")
for vid, sector, status in full_fleet:
    # Update Logistics Side (fleet table)
    cursor.execute("""
        INSERT OR REPLACE INTO fleet (vehicle_id, sector, status, last_updated)
        VALUES (?, ?, ?, ?)
    """, (vid, sector, status, datetime.now()))
    
    # Update Technical Side (gauteng_nodes table)
    cursor.execute("""
        INSERT INTO gauteng_nodes (node_name, node_type, current, target, progress, strategy, recorded_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (vid, 'mobile_node', 879441.26, 50000000.0, 1.75, 'Sovereign Wealth', datetime.now().isoformat()))

conn.commit()
conn.close()
print(f"✅ Mission Success: 17 Vehicles Synchronized at {datetime.now()}")
