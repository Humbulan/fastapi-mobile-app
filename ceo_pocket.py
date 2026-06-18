#!/usr/bin/env python3
from db_config import get_db_connection
"""
💰 CEO POCKET - Sovereign Salary Manager
Tracks 2% management fee from IDC dividends and SADC syncs
"""
import sqlite3
from datetime import datetime
import os

print("💰 CEO POCKET - SOVEREIGN SALARY")
print("="*60)

conn = get_db_connection()
cursor = conn.cursor()

# 1. Create CEO Pocket table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ceo_pocket (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_sector TEXT,
        total_pool REAL,
        ceo_cut_2_percent REAL,
        recorded_at DATETIME,
        status TEXT DEFAULT 'available'
    )
''')

# 2. Calculate IDC dividends total
cursor.execute("SELECT SUM(amount) FROM payment WHERE payment_method IN ('IMPERIAL_WEB_UPGRADE', 'SADC_A_LOGISTICS', 'SADC_B_RETAIL')")
total_idc = cursor.fetchone()[0] or 0
ceo_idc = total_idc * 0.02

# Insert IDC entry
cursor.execute('''
    INSERT INTO ceo_pocket (source_sector, total_pool, ceo_cut_2_percent, recorded_at)
    VALUES (?, ?, ?, ?)
''', ('IDC_DIVIDENDS', total_idc, ceo_idc, datetime.now().isoformat()))

# 3. Calculate SADC syncs (from bridged payments)
cursor.execute("SELECT SUM(amount) FROM payment WHERE payment_method IN ('SADC_A_LOGISTICS', 'SADC_B_RETAIL') AND status='synced'")
total_sadc_synced = cursor.fetchone()[0] or 0
ceo_sadc = total_sadc_synced * 0.02

if total_sadc_synced > 0:
    cursor.execute('''
        INSERT INTO ceo_pocket (source_sector, total_pool, ceo_cut_2_percent, recorded_at)
        VALUES (?, ?, ?, ?)
    ''', ('SADC_SYNCS', total_sadc_synced, ceo_sadc, datetime.now().isoformat()))

conn.commit()

# Show totals
cursor.execute("SELECT SUM(ceo_cut_2_percent) FROM ceo_pocket WHERE status='available'")
total_available = cursor.fetchone()[0] or 0

print(f"\n📊 IDC DIVIDENDS POOL: R{total_idc:,.2f}")
print(f"   👑 Your 2%:         R{ceo_idc:,.2f}")
print(f"\n🚀 SADC SYNCED POOL:  R{total_sadc_synced:,.2f}")
print(f"   👑 Your 2%:         R{ceo_sadc:,.2f}")
print(f"\n💰 TOTAL AVAILABLE:   R{total_available:,.2f}")

# Show recent pocket entries
print(f"\n📋 POCKET HISTORY:")
cursor.execute("SELECT source_sector, total_pool, ceo_cut_2_percent, recorded_at FROM ceo_pocket ORDER BY recorded_at DESC LIMIT 5")
for sector, pool, cut, date in cursor.fetchall():
    print(f"  • {sector}: R{cut:,.2f} from R{pool:,.2f} pool ({date[:10]})")

conn.close()
