#!/usr/bin/env python3
from db_config import get_db_connection
"""
🔍 IMPERIAL REINVESTMENT AUDIT
Tracking IDC Dividends across SADC corridors and Web Upgrade
"""
import sqlite3
from datetime import datetime

print("🔍 AUDITING REINVESTMENT BUCKETS...")
print("="*60)

conn = get_db_connection()
cursor = conn.cursor()

# Search for IMPERIAL_WEB_UPGRADE entries
cursor.execute("""
    SELECT COUNT(*), SUM(amount) 
    FROM payment 
    WHERE payment_method LIKE '%WEB_UPGRADE%' 
       OR payment_method = 'IMPERIAL_WEB_UPGRADE'
""")
web_count, web_total = cursor.fetchone()
web_total = web_total or 0

print(f"\n🌐 WEB UPGRADE SECTOR:")
print(f"   Transactions: {web_count}")
print(f"   Total Capital: R{web_total:,.2f}")
print(f"   Status: {'✅ ACTIVE' if web_count > 0 else '⚠️  NOT FOUND'}")

# Search for SADC_A_LOGISTICS
cursor.execute("""
    SELECT COUNT(*), SUM(amount) 
    FROM payment 
    WHERE payment_method LIKE '%SADC_A_LOGISTICS%'
""")
sadc_a_count, sadc_a_total = cursor.fetchone()
sadc_a_total = sadc_a_total or 0

print(f"\n🚚 SADC_A_LOGISTICS:")
print(f"   Transactions: {sadc_a_count}")
print(f"   Total Capital: R{sadc_a_total:,.2f}")

# Search for SADC_B_RETAIL
cursor.execute("""
    SELECT COUNT(*), SUM(amount) 
    FROM payment 
    WHERE payment_method LIKE '%SADC_B_RETAIL%'
""")
sadc_b_count, sadc_b_total = cursor.fetchone()
sadc_b_total = sadc_b_total or 0

print(f"\n🏪 SADC_B_RETAIL:")
print(f"   Transactions: {sadc_b_count}")
print(f"   Total Capital: R{sadc_b_total:,.2f}")

# Calculate total IDC dividends
total_idc = web_total + sadc_a_total + sadc_b_total
total_tx = web_count + sadc_a_count + sadc_b_count
print(f"\n💰 TOTAL IDC DIVIDENDS TRACKED: R{total_idc:,.2f}")
print(f"📊 TOTAL TRANSACTIONS: {total_tx}")

# Dividend pattern analysis
if total_tx > 0:
    avg_dividend = total_idc / total_tx
    print(f"   Average dividend: R{avg_dividend:,.2f}")

# Ensure sectors exist in system_sectors
cursor.execute("INSERT OR IGNORE INTO system_sectors (port, service_name, status, wealth_value) VALUES (8106, 'IMPERIAL_WEB_UPGRADE', 'online', ?)", (web_total,))
cursor.execute("INSERT OR IGNORE INTO system_sectors (port, service_name, status, wealth_value) VALUES (8107, 'SADC_A_LOGISTICS', 'online', ?)", (sadc_a_total,))
cursor.execute("INSERT OR IGNORE INTO system_sectors (port, service_name, status, wealth_value) VALUES (8108, 'SADC_B_RETAIL', 'online', ?)", (sadc_b_total,))

conn.commit()

print(f"\n✅ Director Updated - New sectors added:")
print(f"   • Port 8106: IMPERIAL_WEB_UPGRADE - R{web_total:,.2f}")
print(f"   • Port 8107: SADC_A_LOGISTICS - R{sadc_a_total:,.2f}")
print(f"   • Port 8108: SADC_B_RETAIL - R{sadc_b_total:,.2f}")

conn.close()

# Create dividend pattern file
with open('idc_dividend_pattern.txt', 'w') as f:
    f.write("IDC DIVIDEND REINVESTMENT PATTERN (Feb 2026)\n")
    f.write("="*50 + "\n")
    f.write("Based on recovered logs - Average dividends every 10 seconds\n")
    f.write(f"Current tracked total: R{total_idc:,.2f}\n")
    f.write(f"Total transactions: {total_tx}\n")
    f.write("\nDistribution:\n")
    f.write(f"  IMPERIAL_WEB_UPGRADE: R{web_total:,.2f}\n")
    f.write(f"  SADC_A_LOGISTICS: R{sadc_a_total:,.2f}\n")
    f.write(f"  SADC_B_RETAIL: R{sadc_b_total:,.2f}\n")

print("\n✅ Audit complete")
