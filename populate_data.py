#!/usr/bin/env python3
from db_config import get_db_connection
"""
Populate database with sample data for Imperial Network 2.0
"""
import sqlite3
import os
from datetime import datetime, timedelta

DATABASE = os.path.join('instance', 'imperial.db')

def populate():
    print("📊 Populating database with sample data...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if we already have data (using correct table name 'user')
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
    if cursor.fetchone():
        cursor.execute("SELECT COUNT(*) FROM user")
        if cursor.fetchone()[0] > 0:
            print("✅ Database already has data. Skipping population.")
            return
    
    # Create tables if they don't exist
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            phone TEXT,
            village TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            customer_id INTEGER NOT NULL,
            description TEXT,
            amount REAL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES user (id)
        );
        
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payment_id TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            amount REAL,
            payment_method TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user (id)
        );
        
        CREATE TABLE IF NOT EXISTS villages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            district TEXT,
            region TEXT,
            population INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            village_id INTEGER NOT NULL,
            name TEXT,
            tier TEXT DEFAULT 'basic',
            monthly_limit INTEGER DEFAULT 10000,
            usage_count INTEGER DEFAULT 0,
            last_used TIMESTAMP,
            expires_at TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (village_id) REFERENCES villages (id)
        );
    ''')
    
    # Insert sample users (using 'user' table)
    users = [
        ('admin', 'admin@imperial.com', 'admin123', 'admin', '0771111111', 'Mvurwi Central'),
        ('village1', 'village1@test.com', 'test123', 'user', '0772222222', 'Guruve South'),
        ('village2', 'village2@test.com', 'test123', 'user', '0773333333', 'Shamva North'),
        ('village3', 'village3@test.com', 'test123', 'user', '0774444444', 'Mvurwi Central'),
    ]
    
    for user in users:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO user (username, email, password, role, phone, village)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', user)
        except Exception as e:
            print(f"Warning: {e}")
    
    # Insert villages
    villages = [
        ('Mvurwi Central', 'Mazowe', 'Mashonaland Central', 15000),
        ('Guruve South', 'Guruve', 'Mashonaland Central', 12000),
        ('Shamva North', 'Shamva', 'Mashonaland Central', 18000),
        ('Bindura Urban', 'Bindura', 'Mashonaland Central', 25000),
    ]
    
    for village in villages:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO villages (name, district, region, population)
                VALUES (?, ?, ?, ?)
            ''', village)
        except Exception as e:
            print(f"Warning: {e}")
    
    # Insert sample API keys
    api_keys = [
        ('IMP_1_sample_key_abc123', 1, 'Production Key', 'premium', 50000),
        ('IMP_2_sample_key_def456', 2, 'Development Key', 'basic', 10000),
        ('IMP_3_sample_key_ghi789', 3, 'Analytics Key', 'enterprise', 100000),
        ('PREMIUM_KEY_A1B2C3D4', 1, 'Legacy Premium Key', 'premium', 1000000),
    ]
    
    for key in api_keys:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO api_keys (key, village_id, name, tier, monthly_limit, expires_at)
                VALUES (?, ?, ?, ?, ?, DATE('now', '+1 year'))
            ''', key)
        except Exception as e:
            print(f"Warning: {e}")
    
    # Insert sample orders
    orders = [
        ('ORD001', 1, 'Maize seeds', 500.00, 'completed'),
        ('ORD002', 2, 'Fertilizer', 1200.00, 'pending'),
        ('ORD003', 3, 'Tools', 350.00, 'completed'),
        ('ORD004', 1, 'Seeds', 750.00, 'processing'),
    ]
    
    for order in orders:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO orders (order_number, customer_id, description, amount, status)
                VALUES (?, ?, ?, ?, ?)
            ''', order)
        except Exception as e:
            print(f"Warning: {e}")
    
    # Insert sample payments
    payments = [
        ('PAY001', 1, 500.00, 'cash', 'completed'),
        ('PAY002', 2, 1200.00, 'mobile', 'pending'),
        ('PAY003', 3, 350.00, 'cash', 'completed'),
    ]
    
    for payment in payments:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO payments (payment_id, user_id, amount, payment_method, status)
                VALUES (?, ?, ?, ?, ?)
            ''', payment)
        except Exception as e:
            print(f"Warning: {e}")
    
    conn.commit()
    
    # Get counts
    cursor.execute("SELECT COUNT(*) FROM user")
    user_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM villages")
    village_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM api_keys")
    key_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM payments")
    payment_count = cursor.fetchone()[0]
    
    conn.close()
    
    print("✅ Sample data populated successfully!")
    print(f"   • {user_count} users added")
    print(f"   • {village_count} villages added")
    print(f"   • {key_count} API keys added")
    print(f"   • {order_count} orders added")
    print(f"   • {payment_count} payments added")

if __name__ == "__main__":
    populate()
