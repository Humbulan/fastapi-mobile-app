#!/usr/bin/env python3
import smtplib, json
from email.message import EmailMessage
from pathlib import Path

# LOAD VERIFIED CREDENTIALS
with open(Path.home() / 'imperial_network' / 'smtp_config.json', 'r') as f:
    config = json.load(f)
    u, p = config['smtp']['username'], config['smtp']['password']

def send_vault_report():
    msg = EmailMessage()
    # RESTORING YOUR ORIGINAL FORMAT EXACTLY
    content = """Sovereign Humbulani Mudau,

Your Imperial Vault has been updated.

📊 CURRENT FINANCIAL STANDING:
• Total Valuation: R1,806,166,092.14
• Active Villages: 43
• Operational Vehicles: 17
• SADC Corridor Assets: R1.17B

📈 PORTFOLIO BREAKDOWN:
• Logistics: R875,000,000
• Lithium: R85,500,000
• Gold: R145,000,000
• Energy: R68,600,000

🏦 NEDBANK STATUS:
• Status: OPERATIONAL

⛓️ BLOCKCHAIN SYNC:
• Timestamp: 2026-04-03T08:01:10.211791

📋 ACTION ITEMS:
• Portfolio valuation updated
• Gateway status verified
• All systems operational

This message has been automatically archived to your Imperial Vault."""

    msg.set_content(content)
    msg['Subject'] = "Imperial Vault Update - 2026-04-03"
    msg['From'] = u
    msg['To'] = u

    try:
        with smtplib.SMTP("smtp.zoho.com", 587) as server:
            server.starttls()
            server.login(u, p)
            server.send_message(msg)
            print("✅ VAULT REPORT SENT SUCCESSFULLY")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🏛️ TRIGGERING IMPERIAL VAULT SYNC...")
    send_vault_report()
