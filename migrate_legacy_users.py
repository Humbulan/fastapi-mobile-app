#!/usr/bin/env python3
"""
Migrate legacy users to Imperial Network schema
Schema: id, username, email, password, role, phone, village, created_at
"""
import csv
import sqlite3
import hashlib
import os
from datetime import datetime
from pathlib import Path

print("🏛️ IMPERIAL LEGACY USER MIGRATION")
print("=" * 60)

# Find the legacy vault
legacy_dirs = [
    Path.home() / "humbu_community_nexus/Imperial_Omega/LEGACY_708_VAULT/OFFICIAL_RECORDS",
    Path.home() / "humbu_community_nexus",
]

vault_file = None
for base_dir in legacy_dirs:
    if base_dir.exists():
        # Look for CSV files
        csv_files = list(base_dir.glob("**/*.csv"))
        for csv_file in csv_files:
            if "user" in csv_file.name.lower() or "master" in csv_file.name.lower() or "directory" in csv_file.name.lower():
                vault_file = csv_file
                print(f"✅ Found potential vault: {vault_file}")
                break

if not vault_file:
    print("❌ Could not find legacy vault")
    print("Please enter the path to the user CSV file:")
    custom_path = input("> ").strip()
    if custom_path and Path(custom_path).exists():
        vault_file = Path(custom_path)
    else:
        exit(1)

print(f"\n📖 Reading from: {vault_file}")

# Connect to Imperial DB
conn = sqlite3.connect('instance/imperial.db')
cursor = conn.cursor()

# Read CSV and prepare users
migrated = 0
skipped = 0
duplicates = 0

with open(vault_file, 'r') as f:
    reader = csv.DictReader(f)
    csv_columns = reader.fieldnames
    print(f"📋 CSV columns: {csv_columns}")
    
    for row in reader:
        try:
            # Extract name (try different possible column names)
            name = None
            for col in ['name', 'Name', 'full_name', 'username', 'NAMES', 'Names']:
                if col in row and row[col]:
                    name = row[col].strip()
                    break
            
            if not name:
                # Try to construct from first/last
                first = row.get('first_name', row.get('First', '')).strip()
                last = row.get('last_name', row.get('Last', '')).strip()
                if first or last:
                    name = f"{first} {last}".strip()
                else:
                    name = "Legacy User"
            
            # Extract phone
            phone = None
            for col in ['phone', 'Phone', 'mobile', 'Mobile', 'cell', 'Cell', 'PHONE']:
                if col in row and row[col]:
                    phone = row[col].strip().replace(' ', '').replace('-', '')
                    break
            
            # Extract village
            village = None
            for col in ['village', 'Village', 'location', 'Location', 'town', 'Town', 'area', 'Area']:
                if col in row and row[col]:
                    village = row[col].strip()
                    break
            
            # Create email from name if not present
            email = None
            for col in ['email', 'Email', 'mail', 'Mail']:
                if col in row and row[col]:
                    email = row[col].strip()
                    break
            
            if not email:
                # Generate email from name
                base = name.lower().replace(' ', '.')
                email = f"{base}@legacy.user"
            
            # Create username (must be unique)
            username_base = name.lower().replace(' ', '_')
            username = username_base
            counter = 1
            
            # Check if username exists
            while True:
                cursor.execute("SELECT id FROM user WHERE username = ?", (username,))
                if not cursor.fetchone():
                    break
                username = f"{username_base}_{counter}"
                counter += 1
            
            # Create default password hash (temporary - users should reset on first login)
            # Using a simple hash of "changeme" + username
            default_password = f"changeme_{username}"
            from auth_utils import hash_password
            password_hash = hash_password(default_password)
            
            # Insert user
            cursor.execute('''
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
            
            if cursor.rowcount > 0:
                migrated += 1
                if migrated <= 10:  # Show first 10
                    print(f"✅ Migrated: {name} -> {username} ({phone}) - {village}")
            else:
                # Check if it was duplicate email or username
                cursor.execute("SELECT id FROM user WHERE email = ?", (email,))
                if cursor.fetchone():
                    duplicates += 1
                    print(f"⏭️  Duplicate email: {email}")
                else:
                    skipped += 1
                    
        except Exception as e:
            print(f"⚠️  Error: {e}")
            skipped += 1

conn.commit()

# Final count
cursor.execute('SELECT COUNT(*) FROM user')
total = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM user WHERE role="user"')
user_count = cursor.fetchone()[0]
conn.close()

print("\n" + "=" * 60)
print("📊 MIGRATION SUMMARY:")
print(f"   ✅ New users migrated: {migrated}")
print(f"   ⏭️  Duplicates (email conflict): {duplicates}")
print(f"   ⚠️  Skipped (other errors): {skipped}")
print(f"   📈 Total users in DB: {total}")
print(f"   👤 Regular users: {user_count}")
print(f"   👑 Admin users: {total - user_count}")

# Create a restoration report
with open("legacy_restoration_report.txt", 'w') as f:
    f.write(f"IMPERIAL LEGACY RESTORATION - {datetime.now().isoformat()}\n")
    f.write("=" * 50 + "\n")
    f.write(f"Source: {vault_file}\n")
    f.write(f"Users Migrated: {migrated}\n")
    f.write(f"Total Users Now: {total}\n")
    f.write(f"Regular Users: {user_count}\n")

print(f"\n📄 Report saved to: legacy_restoration_report.txt")
print("\n🔑 Default passwords: 'changeme_username' (users should change on first login)")
