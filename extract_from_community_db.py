#!/usr/bin/env python3
"""
Extract users from community_nexus.db and import to Imperial Network
"""
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path

print("🏛️ EXTRACTING USERS FROM COMMUNITY NEXUS DB")
print("=" * 60)

# Path to community database
community_db = Path.home() / "humbu_community_nexus/community_nexus.db"

if not community_db.exists():
    print(f"❌ Community database not found at {community_db}")
    exit(1)

print(f"✅ Found community database: {community_db}")

# Connect to community database
comm_conn = sqlite3.connect(str(community_db))
comm_cursor = comm_conn.cursor()

# Check what tables exist
comm_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = comm_cursor.fetchall()
print(f"\n📋 Tables in community database:")
for table in tables:
    print(f"   - {table[0]}")

# Look for users table
if ('users',) in tables:
    # Check users table schema
    comm_cursor.execute("PRAGMA table_info(users)")
    columns = comm_cursor.fetchall()
    print(f"\n📊 Users table schema:")
    for col in columns:
        print(f"   {col[1]}: {col[2]}")
    
    # Extract all users
    comm_cursor.execute("SELECT * FROM users")
    community_users = comm_cursor.fetchall()
    print(f"\n👥 Found {len(community_users)} users in community database")
    
    # Get column names
    col_names = [col[1] for col in columns]
    
    # Connect to Imperial DB
    imperial_conn = sqlite3.connect('instance/imperial.db')
    imperial_cursor = imperial_conn.cursor()
    
    # Import users
    imported = 0
    skipped = 0
    
    print("\n📥 Importing to Imperial Network...")
    
    for user in community_users:
        user_dict = dict(zip(col_names, user))
        
        # Extract fields (adapt to your actual column names)
        name = user_dict.get('name') or user_dict.get('username') or user_dict.get('full_name') or 'Unknown'
        phone = user_dict.get('phone') or user_dict.get('mobile') or ''
        email = user_dict.get('email') or f"{name.lower().replace(' ', '.')}@community.user"
        village = user_dict.get('village') or user_dict.get('location') or ''
        
        # Clean phone
        if phone:
            phone = str(phone).replace(' ', '').replace('-', '')
        
        # Create username
        username = name.lower().replace(' ', '_')
        base_username = username
        counter = 1
        
        # Check for uniqueness
        while True:
            imperial_cursor.execute("SELECT id FROM user WHERE username = ?", (username,))
            if not imperial_cursor.fetchone():
                break
            username = f"{base_username}_{counter}"
            counter += 1
        
        # Create password hash
        default_password = f"changeme_{username}"
        from auth_utils import hash_password
        password_hash = hash_password(default_password)
        
        # Insert
        try:
            imperial_cursor.execute('''
                INSERT OR IGNORE INTO user 
                (username, email, password, role, phone, village, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                username,
                email,
                password_hash,
                'user',
                phone,
                village,
                datetime.now().isoformat()
            ))
            
            if imperial_cursor.rowcount > 0:
                imported += 1
                if imported <= 10:
                    print(f"   ✅ {name} -> {username} ({phone})")
            else:
                skipped += 1
                
        except Exception as e:
            print(f"   ⚠️ Error with {name}: {e}")
            skipped += 1
    
    imperial_conn.commit()
    
    # Final counts
    imperial_cursor.execute('SELECT COUNT(*) FROM user')
    total = imperial_cursor.fetchone()[0]
    
    print("\n" + "=" * 60)
    print("📊 MIGRATION SUMMARY:")
    print(f"   ✅ Imported: {imported}")
    print(f"   ⏭️  Skipped: {skipped}")
    print(f"   📈 Total users in Imperial DB: {total}")
    
    # Show sample of new users
    if imported > 0:
        imperial_cursor.execute('SELECT username, phone, village FROM user ORDER BY id DESC LIMIT 5')
        samples = imperial_cursor.fetchall()
        print("\n📋 Recent imports:")
        for sample in samples:
            print(f"   - {sample[0]} ({sample[1]}) - {sample[2]}")
    
    imperial_conn.close()
    
else:
    print("\n❌ No users table found in community database")
    
    # Check other possible tables
    for table in tables:
        table_name = table[0]
        comm_cursor.execute(f"PRAGMA table_info({table_name})")
        cols = comm_cursor.fetchall()
        col_names = [c[1] for c in cols]
        
        if 'phone' in col_names or 'email' in col_names or 'name' in col_names:
            print(f"\n🔍 Table '{table_name}' might contain user data:")
            print(f"   Columns: {col_names}")
            
            # Sample data
            comm_cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            samples = comm_cursor.fetchall()
            for sample in samples:
                print(f"   Sample: {sample}")

comm_conn.close()
