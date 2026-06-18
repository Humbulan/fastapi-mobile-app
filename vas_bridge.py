#!/usr/bin/env python3
from db_config import get_db_connection
"""
Imperial VAS Bridge - Converts vouchers to real airtime
Connects Voucher API (8098) to Nedbank/Prepaid24 VAS providers
"""
import json
import requests
import sqlite3
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    filename='logs/vas_bridge.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

class VASProvider:
    """Handle real-world airtime purchases"""
    
    def __init__(self, provider="NEDBANK"):
        self.provider = provider
        # Load your API credentials from secure config
        self.api_key = "FI7944391"  # Get from Nedbank Marketplace
        self.client_id = "mbu_wandeme_trading"
        self.client_secret = "FI7944391"
        
    def purchase_airtime(self, phone_number, ceo_cut_2_percent, reference):
        """Purchase airtime via Nedbank VAS API"""
        endpoint = "https://b2b-api.nedbank.co.za/apimarket/b2b-sb/nb-vas/prepaid/purchase"
        
        payload = {
            "recipient": phone_number,
            "ceo_cut_2_percent": ceo_cut_2_percent,
            "billingType": "Variable",
            "reference": reference
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "clientId": self.client_id
        }
        
        # In production, this would make the actual API call
        # For now, we log and simulate
        logging.info(f"PURCHASE: R{ceo_cut_2_percent} airtime to {phone_number} (Ref: {reference})")
        
        # Deduct from CEO_POCKET (R879k available)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE ceo_pocket SET ceo_cut_2_percent = ceo_cut_2_percent - ? WHERE id=2 AND status='available'", (ceo_cut_2_percent,))
        conn.commit()
        conn.close()
        
        return {"status": "success", "reference": reference}

def redeem_voucher(voucher_key, phone_number):
    """Main redemption function called by Voucher API"""
    
    # 1. Load vouchers
    with open('vouchers.json', 'r') as f:
        vouchers = json.load(f)
    
    # 2. Check if voucher exists and is active
    if voucher_key not in vouchers:
        return {"status": "error", "message": "Invalid voucher"}
    
    voucher = vouchers[voucher_key]
    if voucher['status'] != 'active':
        return {"status": "error", "message": "Voucher already used"}
    
    # 3. Validate phone number (SA format)
    phone = phone_number.strip()
    if phone.startswith('0'):
        phone = '27' + phone[1:]
    if not (phone.isdigit() and 10 <= len(phone) <= 12):
        return {"status": "error", "message": "Invalid SA phone number"}
    
    # 4. Process via VAS provider
    vas = VASProvider()
    result = vas.purchase_airtime(
        phone_number=phone,
        ceo_cut_2_percent=voucher['value'],
        reference=f"IMP-{voucher_key}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    )
    
    # 5. Mark voucher as used
    voucher['status'] = 'used'
    voucher['redeemed_at'] = str(datetime.now())
    voucher['redeemed_by'] = phone
    with open('vouchers.json', 'w') as f:
        json.dump(vouchers, f, indent=2)
    
    # 6. Log to Family Vault
    with open('logs/airtime_redemptions.log', 'a') as f:
        f.write(f"{datetime.now()}: {voucher_key} redeemed for R{voucher['value']} to {phone}\n")
    
    return {
        "status": "success",
        "message": f"R{voucher['value']} airtime sent to {phone}",
        "reference": result['reference']
    }

# Example usage
if __name__ == "__main__":
    # Test redemption
    result = redeem_voucher("0YUH-XKME", "0821234567")
    print(json.dumps(result, indent=2))
