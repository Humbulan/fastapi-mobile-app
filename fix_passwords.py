#!/usr/bin/env python3
from db_config import get_db_connection
from Crypto.Hash import SHA256
import sqlite3

def hash_password(password):
    """Same hash function as in app.py"""
    return SHA256.new(password.encode()).hexdigest()

# Connect to database
conn = get_db_connection()
cursor = conn.cursor()

# Update admin password
admin_hash = hash_password('admin123')
cursor.execute("UPDATE user SET password = ? WHERE email = 'admin@imperial.com'", (admin_hash,))
print(f"Admin password updated to: {admin_hash}")

# Update test users
test_hash = hash_password('test123')
for email in ['village1@test.com', 'village2@test.com', 'village3@test.com']:
    cursor.execute("UPDATE user SET password = ? WHERE email = ?", (test_hash, email))
    print(f"{email} password updated")

# Commit changes
conn.commit()
conn.close()
print("\n✅ Passwords updated successfully!")
