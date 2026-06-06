#!/usr/bin/env python3
import sqlite3

def reconcile():
    db_path = "/data/data/com.termux/files/home/imperial_network/instance/imperial.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, payment_method FROM payment WHERE status='pending';")
    pending = cursor.fetchall()
    
    if pending:
        print(f"🛠️ Found {len(pending)} pending records. Reconciling...")
        cursor.execute("UPDATE payment SET status='completed' WHERE status='pending';")
        conn.commit()
        print("✅ Reconciliation Complete. Ledger updated.")
    else:
        print("✅ No pending records found.")
    
    conn.close()

if __name__ == "__main__":
    reconcile()
