from db_config import get_db_connection
import sqlite3
import os
from datetime import datetime, timedelta
import random

# 1. DATABASE SETUP
db_path = 'instance/imperial.db'
os.makedirs('instance', exist_ok=True)
conn = get_db_connection()
cursor = conn.cursor()
cursor.row_factory = sqlite3.Row

# 2. CREATE TABLES IF NOT EXISTS
cursor.execute("""
CREATE TABLE IF NOT EXISTS village (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    district TEXT,
    region TEXT,
    population INTEGER,
    created_at TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS api_key (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE,
    village_id INTEGER,
    name TEXT,
    tier TEXT,
    monthly_limit INTEGER,
    usage_count INTEGER DEFAULT 0,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP,
    FOREIGN KEY (village_id) REFERENCES village (id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT,
    phone TEXT,
    village TEXT,
    created_at TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS payment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_id TEXT UNIQUE,
    user_id INTEGER,
    amount REAL,
    payment_method TEXT,
    status TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT UNIQUE,
    customer_id INTEGER,
    description TEXT,
    amount REAL,
    status TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES user (id)
)
""")

# 3. THE ABSOLUTE TRUTH: DATA PAYLOAD
villages = [
    ('Matsila', 'Malamulele', 'Limpopo', 12500, datetime.now()),
    ('Altein', 'Malamulele', 'Limpopo', 8200, datetime.now()),
    ('Ka-Mahonisi', 'Malamulele', 'Limpopo', 5400, datetime.now()),
    ('Gumbani', 'Malamulele', 'Limpopo', 6300, datetime.now()),
    ('Mukhomi', 'Malamulele', 'Limpopo', 7100, datetime.now()),
    ('Bindura Urban', 'Bindura', 'Mashonaland Central', 25000, datetime.now()),
    ('Guruve South', 'Guruve', 'Mashonaland Central', 12000, datetime.now()),
    ('Mvurwi Central', 'Mazowe', 'Mashonaland Central', 15000, datetime.now()),
    ('Shamva North', 'Shamva', 'Mashonaland Central', 18000, datetime.now()),
    ('Malamulele Plaza', 'Malamulele', 'Limpopo', 500, datetime.now()),
    ('Masingita Crossing', 'Malamulele', 'Limpopo', 350, datetime.now())
]

# 4. INJECTION
print("📡 Injecting Village Grid...")
for village in villages:
    cursor.execute("""
        INSERT OR IGNORE INTO village (name, district, region, population, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, village)

# 5. GENERATE API KEYS FOR EACH VILLAGE
print("🔑 Generating API Keys...")
cursor.execute("SELECT id, name FROM village")
all_villages = cursor.fetchall()

tiers = ['basic', 'premium', 'enterprise']
limits = {'basic': 10000, 'premium': 50000, 'enterprise': 100000}

for village in all_villages:
    # Generate 2-3 keys per village
    for i in range(random.randint(2, 3)):
        key_name = f"{village['name']} Key {i+1}"
        tier = random.choice(tiers)
        key = f"IMP_{village['name'].replace(' ', '_').upper()}_{random.randint(1000, 9999)}_{os.urandom(4).hex().upper()}"
        
        cursor.execute("""
            INSERT OR IGNORE INTO api_key 
            (key, village_id, name, tier, monthly_limit, usage_count, expires_at, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            key,
            village['id'],
            key_name,
            tier,
            limits[tier],
            random.randint(0, 5000),
            datetime.now() + timedelta(days=365),
            1,
            datetime.now()
        ))

# 6. CREATE FLEET TRACKING TABLE (for your IMP vehicles)
cursor.execute("""
CREATE TABLE IF NOT EXISTS fleet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id TEXT UNIQUE,
    sector TEXT,
    status TEXT,
    last_updated TIMESTAMP
)
""")

fleet = [
    ('IMP-01', 'Malamulele Plaza', 'Active - CEO Escort', datetime.now()),
    ('IMP-02', 'Masingita Crossing', 'Active - R15M Audit', datetime.now()),
    ('IMP-15', 'Mukhomi', 'Patrol', datetime.now()),
    ('IMP-16', 'Gumbani', 'Relay', datetime.now()),
    ('IMP-03', 'Bindura Urban', 'Standby', datetime.now()),
    ('IMP-04', 'Shamva North', 'Maintenance', datetime.now())
]

print("🚛 Commissioning Fleet...")
for vehicle in fleet:
    cursor.execute("""
        INSERT OR IGNORE INTO fleet (vehicle_id, sector, status, last_updated)
        VALUES (?, ?, ?, ?)
    """, vehicle)

conn.commit()

# 7. VERIFICATION
print("\n" + "="*50)
print("🏆 IMPERIAL NETWORK RESTORATION REPORT")
print("="*50)

cursor.execute("SELECT COUNT(*) as count FROM village")
print(f"🏘️ Villages: {cursor.fetchone()['count']}")

cursor.execute("SELECT COUNT(*) as count FROM api_key")
print(f"🔑 API Keys: {cursor.fetchone()['count']}")

cursor.execute("SELECT COUNT(*) as count FROM fleet")
print(f"🚛 Fleet Vehicles: {cursor.fetchone()['count']}")

cursor.execute("SELECT name FROM village LIMIT 5")
villages_list = cursor.fetchall()
print(f"\n📋 Sample Villages: {', '.join([v['name'] for v in villages_list])}")

cursor.execute("SELECT vehicle_id, status FROM fleet LIMIT 3")
fleet_list = cursor.fetchall()
print(f"🚗 Sample Fleet: {', '.join([f['vehicle_id'] for f in fleet_list])}")

conn.close()
print("\n✅ Data injection complete! Your Imperial Network is now populated.")
