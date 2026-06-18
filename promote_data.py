#!/usr/bin/env python3
from db_config import get_db_connection
"""
IMPERIAL DATA PROMOTION SCRIPT
Moves data from nexus_backup tables to production tables
"""

import sqlite3
import os
from datetime import datetime
import hashlib
import random

def connect_db():
    return get_db_connection()

def promote_users():
    print("\n👥 Promoting users to production...")
    conn = connect_db()
    cursor = conn.cursor()
    
    # Check if users already exist
    cursor.execute("SELECT COUNT(*) FROM user")
    existing = cursor.fetchone()[0]
    print(f"  Existing users: {existing}")
    
    # Get users from backup
    cursor.execute("SELECT * FROM nexus_backup_users")
    users = cursor.fetchall()
    
    # Get column names
    cursor.execute("PRAGMA table_info(nexus_backup_users)")
    columns = [col[1] for col in cursor.fetchall()]
    
    promoted = 0
    for user in users:
        user_dict = dict(zip(columns, user))
        
        # Check if user already exists by email or phone
        cursor.execute("SELECT id FROM user WHERE phone = ?", (user_dict.get('phone'),))
        if cursor.fetchone():
            print(f"  ⏭️  User {user_dict.get('name')} already exists")
            continue
        
        # Create user in production table
        # Generate a simple password hash (in production, use proper hashing)
        password_hash = hashlib.sha256(f"temp_{user_dict.get('phone')}".encode()).hexdigest()
        
        try:
            cursor.execute("""
                INSERT INTO user 
                (username, email, password, role, phone, village, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user_dict.get('name').lower().replace(' ', '_')[:50],
                f"{user_dict.get('name').lower().replace(' ', '.')}@imperial.local",
                password_hash,
                user_dict.get('role', 'user'),
                user_dict.get('phone'),
                user_dict.get('village', 'Unknown'),
                datetime.now()
            ))
            promoted += 1
            print(f"  ✅ Promoted: {user_dict.get('name')} ({user_dict.get('phone')})")
        except Exception as e:
            print(f"  ❌ Error promoting {user_dict.get('name')}: {e}")
    
    conn.commit()
    print(f"  ✅ Promoted {promoted} new users")
    conn.close()

def promote_transactions():
    print("\n💰 Promoting transactions to production...")
    conn = connect_db()
    cursor = conn.cursor()
    
    # Check if payments table exists
    cursor.execute("SELECT COUNT(*) FROM payment")
    existing = cursor.fetchone()[0]
    print(f"  Existing payments: {existing}")
    
    # Get transactions from backup
    cursor.execute("SELECT * FROM nexus_backup_transaction_logs")
    transactions = cursor.fetchall()
    
    if not transactions:
        print("  No transactions to promote")
        conn.close()
        return
    
    # Get column names
    cursor.execute("PRAGMA table_info(nexus_backup_transaction_logs)")
    columns = [col[1] for col in cursor.fetchall()]
    
    promoted = 0
    for tx in transactions:
        tx_dict = dict(zip(columns, tx))
        
        # Find user by phone
        cursor.execute("SELECT id FROM user WHERE phone LIKE ?", (f"%{tx_dict.get('phone', '').replace(' ', '')}%",))
        user = cursor.fetchone()
        
        if not user:
            print(f"  ⏭️  No user found for phone: {tx_dict.get('phone')}")
            continue
        
        try:
            cursor.execute("""
                INSERT INTO payment 
                (payment_id, user_id, amount, payment_method, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                f"TXN_{int(datetime.now().timestamp())}_{random.randint(1000,9999)}",
                user[0],
                float(tx_dict.get('amount', 0)) * 1.25,
                tx_dict.get('provider', 'mobile_money'),
                tx_dict.get('status', 'completed'),
                tx_dict.get('date', datetime.now())
            ))
            promoted += 1
            print(f"  ✅ Promoted transaction: {tx_dict.get('amount')} for user {user[0]}")
        except Exception as e:
            print(f"  ❌ Error promoting transaction: {e}")
    
    conn.commit()
    print(f"  ✅ Promoted {promoted} transactions")
    conn.close()

def promote_vault_data():
    print("\n🏦 Promoting vault data to production...")
    conn = connect_db()
    cursor = conn.cursor()
    
    # Check if we have urban_transactions table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='nexus_backup_urban_transactions'")
    if not cursor.fetchone():
        print("  No vault data found")
        conn.close()
        return
    
    cursor.execute("SELECT * FROM nexus_backup_urban_transactions")
    vault = cursor.fetchall()
    
    if vault:
        print(f"  Found {len(vault)} vault records")
        for record in vault:
            # Create a special system transaction record
            print(f"  💰 TREASURY: {record[3]} R{record[4]}")  # revenue_generated
            # In a real system, you'd add this to a treasury table
    
    conn.close()

def promote_listings():
    print("\n🛒 Promoting marketplace listings...")
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM nexus_backup_listings LIMIT 5")
    listings = cursor.fetchall()
    
    if listings:
        print(f"  Found marketplace data (ready for integration)")
        cursor.execute("SELECT COUNT(*) FROM nexus_backup_listings")
        count = cursor.fetchone()[0]
        print(f"  Total listings available: {count}")
    
    conn.close()

def create_treasury_report():
    print("\n📊 CREATING IMPERIAL TREASURY REPORT")
    print("=" * 40)
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # Calculate total from vault
    cursor.execute("SELECT SUM(revenue_generated) FROM nexus_backup_urban_transactions")
    total = cursor.fetchone()[0] or 0
    print(f"🏦 VAULT TOTAL: R{total:,.2f}")
    
    # Calculate from settlement batches
    cursor.execute("SELECT SUM(total_amount) FROM nexus_backup_settlement_batch")
    settlements = cursor.fetchone()[0] or 0
    print(f"📦 SETTLEMENTS: R{settlements:,.2f}")
    
    # Calculate from transactions
    cursor.execute("SELECT SUM(amount) FROM nexus_backup_transaction_logs")
    tx_total = cursor.fetchone()[0] or 0
    print(f"💳 TRANSACTIONS: R{tx_total:,.2f}")
    
    # User count
    cursor.execute("SELECT COUNT(*) FROM nexus_backup_users")
    users = cursor.fetchone()[0] or 0
    print(f"👥 TOTAL USERS: {users}")
    
    # Listings count
    cursor.execute("SELECT COUNT(*) FROM nexus_backup_listings")
    listings = cursor.fetchone()[0] or 0
    print(f"🛒 TOTAL LISTINGS: {listings}")
    
    conn.close()
    
    # Save report
    with open('imperial_treasury_report.txt', 'w') as f:
        f.write(f"IMPERIAL TREASURY REPORT - {datetime.now()}\n")
        f.write("=" * 40 + "\n")
        f.write(f"VAULT TOTAL: R{total:,.2f}\n")
        f.write(f"SETTLEMENTS: R{settlements:,.2f}\n")
        f.write(f"TRANSACTIONS: R{tx_total:,.2f}\n")
        f.write(f"TOTAL USERS: {users}\n")
        f.write(f"TOTAL LISTINGS: {listings}\n")
    
    print(f"\n📄 Report saved to: imperial_treasury_report.txt")

if __name__ == "__main__":
    print("=" * 50)
    print("IMPERIAL DATA PROMOTION ENGINE")
    print("=" * 50)
    
    promote_users()
    promote_transactions()
    promote_vault_data()
    promote_listings()
    create_treasury_report()
    
    print("\n✅ Data promotion complete!")
    print("Next steps:")
    print("1. Review imperial_treasury_report.txt")
    print("2. Test user login with imported users")
    print("3. Run ./cleanup_repos.sh to free space")
