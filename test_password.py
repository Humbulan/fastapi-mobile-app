#!/usr/bin/env python3
from db_config import get_db_connection
import hashlib
import sqlite3

def hash_password(password):
    """Simple SHA-256 hashing for passwords"""
    return hashlib.sha256(password.encode()).hexdigest()

# Test password
test_password = "admin123"
hashed = hash_password(test_password)
print(f"Password '{test_password}' hashes to: {hashed}")

# Check database
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT email, password FROM user")
for email, password in cursor.fetchall():
    print(f"User: {email}")
    print(f"  Stored hash: {password}")
    print(f"  Hash of 'admin123': {hashed}")
    print(f"  Match: {password == hashed}")
    print()
conn.close()
