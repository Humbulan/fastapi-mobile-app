#!/usr/bin/env python3
from db_config import get_db_connection
"""
Database migration script for Imperial Network 2.0
Adds villages, api_keys, and api_usage_logs tables
"""

import sqlite3
import os

DATABASE = os.path.join('instance', 'imperial.db')

def run_migration():
    print("🚀 Starting database migration...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create villages table
    print("📦 Creating villages table...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS villages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            district TEXT,
            region TEXT,
            population INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create api_keys table
    print("🔑 Creating api_keys table...")
    cursor.execute('''
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
        )
    ''')
    
    # Create api_usage_logs table
    print("📊 Creating api_usage_logs table...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_usage_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_key_id INTEGER,
            endpoint TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            response_time INTEGER,
            status_code INTEGER,
            FOREIGN KEY (api_key_id) REFERENCES api_keys (id)
        )
    ''')
    
    # Insert sample villages
    print("🏘️ Adding sample villages...")
    villages = [
        ('Mvurwi Central', 'Mazowe', 'Mashonaland Central', 15000),
        ('Guruve South', 'Guruve', 'Mashonaland Central', 12000),
        ('Shamva North', 'Shamva', 'Mashonaland Central', 18000),
        ('Bindura Urban', 'Bindura', 'Mashonaland Central', 25000),
        ('Mount Darwin East', 'Mount Darwin', 'Mashonaland Central', 9000),
    ]
    
    for village in villages:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO villages (name, district, region, population)
                VALUES (?, ?, ?, ?)
            ''', village)
        except Exception as e:
            print(f"  ⚠️  Error adding {village[0]}: {e}")
    
    # Generate some sample API keys
    print("🔐 Generating sample API keys...")
    sample_keys = [
        ('IMP_1_sample_key_abc123', 1, 'Production Key', 'premium', 50000),
        ('IMP_2_sample_key_def456', 2, 'Development Key', 'basic', 10000),
        ('IMP_3_sample_key_ghi789', 3, 'Analytics Key', 'enterprise', 100000),
    ]
    
    for key in sample_keys:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO api_keys (key, village_id, name, tier, monthly_limit)
                VALUES (?, ?, ?, ?, ?)
            ''', key)
        except Exception as e:
            print(f"  ⚠️  Error adding key: {e}")
    
    conn.commit()
    conn.close()
    
    print("✅ Migration completed successfully!")
    print("\nNew tables created:")
    print("  • villages - Village management")
    print("  • api_keys - API key management") 
    print("  • api_usage_logs - Usage tracking")
    print("\nSample data added for testing!")

if __name__ == "__main__":
    run_migration()
