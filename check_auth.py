import sqlite3, os
try:
    conn = sqlite3.connect('/data/data/com.termux/files/home/imperial_network/instance/imperial.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users LIMIT 1")
    row = cursor.fetchone()
    if row and row[0].startswith('$argon2id$'):
        print("✅ AUTHENTICATION: Argon2id hashing confirmed.")
    else:
        print("⚠️ AUTHENTICATION: Check hash format (Found: " + str(row[0][:15]) + "...)")
    conn.close()
except Exception as e:
    print("❌ ERROR: Could not verify DB: " + str(e))
