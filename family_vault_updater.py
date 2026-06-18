#!/usr/bin/env python3
from db_config import get_db_connection
"""
🏠 IMPERIAL FAMILY VAULT UPDATER
Creates wife-accessible financial records in shared storage
"""
import sqlite3
import os
import shutil
from datetime import datetime

print("🏠 IMPERIAL FAMILY VAULT UPDATER")
print("="*60)

# Connect to database
conn = get_db_connection()
cursor = conn.cursor()

# Get current pocket status
cursor.execute("SELECT SUM(ceo_cut_2_percent) FROM ceo_pocket WHERE status='available'")
available = cursor.fetchone()[0] or 0

# Get breakdown
cursor.execute("SELECT source_sector, SUM(ceo_cut_2_percent) FROM ceo_pocket WHERE status='available' GROUP BY source_sector")
breakdown = cursor.fetchall()

# Calculate family metrics
daily_budget = available / 30
monthly_fund = available / 12
school_terms = available / 20000
next_milestone = ((int(available // 10000) + 1) * 10000)
remaining = next_milestone - available

# Create family statement
statement_file = f"/sdcard/Download/Imperial_Family_Vault/Monthly_Statements/family_statement_{datetime.now().strftime('%Y%m')}.txt"
with open(statement_file, 'w') as f:
    f.write("="*60 + "\n")
    f.write("🏠 IMPERIAL FAMILY VAULT - MONTHLY STATEMENT\n")
    f.write(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("="*60 + "\n\n")
    f.write(f"💰 TOTAL AVAILABLE: R{available:,.2f}\n\n")
    f.write("📊 BREAKDOWN:\n")
    for source, amount in breakdown:
        f.write(f"  • {source}: R{amount:,.2f}\n")
    f.write("\n" + "="*60 + "\n")
    f.write("🏠 FAMILY BUDGET:\n")
    f.write(f"  • Daily Household Budget: R{daily_budget:,.2f}\n")
    f.write(f"  • Monthly Family Fund: R{monthly_fund:,.2f}\n")
    f.write(f"  • School Fees Covered: {school_terms:.1f} terms\n")
    f.write(f"  • Next Milestone: R{next_milestone:,.2f} (R{remaining:,.2f} to go)\n")
    f.write("\n" + "="*60 + "\n")
    f.write("🏛️ IMPERIAL NETWORK\n")
    f.write("CIPC: 2026/1730663/07\n")
    f.write("Sovereign: Humbulani Mudau\n")
    f.write("="*60 + "\n")

# Copy latest withdrawal slip
os.system("cp -f ~/imperial_vault/withdrawal_*.txt /sdcard/Download/Imperial_Family_Vault/Withdrawal_Slips/ 2>/dev/null || true")

# Create school fees tracker
school_file = f"/sdcard/Download/Imperial_Family_Vault/School_Fees/school_tracker_{datetime.now().strftime('%Y')}.txt"
with open(school_file, 'a') as f:
    f.write(f"{datetime.now().strftime('%Y-%m-%d')} | Terms Secured: {school_terms:.1f} | Fund: R{available:,.2f}\n")

# Create household budget tracker
budget_file = f"/sdcard/Download/Imperial_Family_Vault/Household_Budget/budget_{datetime.now().strftime('%Y%m')}.txt"
with open(budget_file, 'w') as f:
    f.write(f"🏠 HOUSEHOLD BUDGET - {datetime.now().strftime('%B %Y')}\n")
    f.write("="*40 + "\n")
    f.write(f"Monthly Allocation: R{monthly_fund:,.2f}\n")
    f.write(f"Weekly: R{monthly_fund/4:,.2f}\n")
    f.write(f"Daily: R{daily_budget:,.2f}\n")

print(f"\n✅ Family Vault updated:")
print(f"  • Statement: {statement_file}")
print(f"  • School Fees: {school_terms:.1f} terms")
print(f"  • Monthly Budget: R{monthly_fund:,.2f}")

# Show files in vault
print(f"\n📁 VAULT CONTENTS:")
os.system("ls -la /sdcard/Download/Imperial_Family_Vault/*/* 2>/dev/null | head -10")

conn.close()
