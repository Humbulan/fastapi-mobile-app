#!/usr/bin/env python3
from db_config import get_db_connection
"""
🎫 Imperial Voucher System - Pay-per-use AI Access
Generate and manage R20 AI access codes
"""
import sqlite3
import random
import string
import hashlib
from datetime import datetime, timedelta
import json
from pathlib import Path

class VoucherSystem:
    def __init__(self, db_path='vouchers.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create voucher database if it doesn't exist"""
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS vouchers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE,
                value INTEGER DEFAULT 20,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP,
                expires_at TIMESTAMP,
                activated_at TIMESTAMP,
                used_by TEXT,
                used_count INTEGER DEFAULT 0,
                max_uses INTEGER DEFAULT 1,
                notes TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS usage_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voucher_code TEXT,
                timestamp TIMESTAMP,
                session_minutes INTEGER,
                ip_address TEXT,
                FOREIGN KEY (voucher_code) REFERENCES vouchers(code)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                price_per_session INTEGER DEFAULT 20,
                session_minutes INTEGER DEFAULT 30,
                currency TEXT DEFAULT 'ZAR',
                updated_at TIMESTAMP
            )
        ''')
        
        # Set default rate if not exists
        c.execute("SELECT COUNT(*) FROM rates")
        if c.fetchone()[0] == 0:
            c.execute("INSERT INTO rates (price_per_session, session_minutes, updated_at) VALUES (20, 30, ?)", 
                     (datetime.now().isoformat(),))
        
        conn.commit()
        conn.close()
        print("✅ Voucher database initialized")
    
    def generate_code(self, length=8):
        """Generate a unique voucher code"""
        chars = string.ascii_uppercase + string.digits
        while True:
            code = ''.join(random.choices(chars, k=length))
            # Format as XXXX-XXXX
            formatted = f"{code[:4]}-{code[4:]}"
            
            # Check if unique
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("SELECT id FROM vouchers WHERE code=?", (formatted,))
            exists = c.fetchone()
            conn.close()
            
            if not exists:
                return formatted
    
    def create_voucher(self, value=20, max_uses=1, notes=''):
        """Create a new voucher"""
        code = self.generate_code()
        created = datetime.now()
        expires = created + timedelta(days=30)  # Valid for 30 days
        
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO vouchers (code, value, created_at, expires_at, max_uses, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (code, value, created.isoformat(), expires.isoformat(), max_uses, notes))
        conn.commit()
        conn.close()
        
        return code
    
    def create_batch(self, count=10, value=20):
        """Create multiple vouchers at once"""
        codes = []
        for i in range(count):
            code = self.create_voucher(value, notes=f'Batch {datetime.now().strftime("%Y%m%d")}')
            codes.append(code)
        return codes
    
    def validate_voucher(self, code):
        """Check if a voucher is valid"""
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            SELECT id, value, status, used_count, max_uses, expires_at 
            FROM vouchers WHERE code=?
        ''', (code,))
        result = c.fetchone()
        conn.close()
        
        if not result:
            return {'valid': False, 'reason': 'Invalid code'}
        
        id, value, status, used_count, max_uses, expires_at = result
        
        if status != 'active':
            return {'valid': False, 'reason': f'Voucher is {status}'}
        
        if used_count >= max_uses:
            return {'valid': False, 'reason': 'Maximum uses reached'}
        
        expires = datetime.fromisoformat(expires_at)
        if expires < datetime.now():
            return {'valid': False, 'reason': 'Voucher expired'}
        
        return {
            'valid': True,
            'id': id,
            'value': value,
            'remaining_uses': max_uses - used_count
        }
    
    def use_voucher(self, code, ip_address='', minutes=30):
        """Mark a voucher as used"""
        validation = self.validate_voucher(code)
        if not validation['valid']:
            return validation
        
        conn = get_db_connection()
        c = conn.cursor()
        
        # Update voucher
        c.execute('''
            UPDATE vouchers 
            SET used_count = used_count + 1,
                activated_at = ?,
                used_by = ?
            WHERE code = ?
        ''', (datetime.now().isoformat(), ip_address, code))
        
        # Log usage
        c.execute('''
            INSERT INTO usage_log (voucher_code, timestamp, session_minutes, ip_address)
            VALUES (?, ?, ?, ?)
        ''', (code, datetime.now().isoformat(), minutes, ip_address))
        
        conn.commit()
        conn.close()
        
        return {'success': True, 'message': 'Voucher activated', 'minutes': minutes}
    
    def get_stats(self):
        """Get voucher statistics"""
        conn = get_db_connection()
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM vouchers")
        total = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM vouchers WHERE status='active'")
        active = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM vouchers WHERE used_count > 0")
        used = c.fetchone()[0]
        
        c.execute("SELECT SUM(value) FROM vouchers WHERE used_count > 0")
        revenue = c.fetchone()[0] or 0
        
        c.execute("SELECT COUNT(*) FROM usage_log WHERE timestamp > date('now', '-7 days')")
        weekly_uses = c.fetchone()[0]
        
        conn.close()
        
        return {
            'total_vouchers': total,
            'active': active,
            'used': used,
            'revenue_zar': revenue,
            'weekly_uses': weekly_uses
        }
    
    def list_active(self):
        """List all active vouchers"""
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            SELECT code, value, created_at, expires_at, used_count, max_uses
            FROM vouchers 
            WHERE status='active' AND used_count < max_uses AND expires_at > datetime('now')
            ORDER BY created_at DESC
        ''')
        vouchers = c.fetchall()
        conn.close()
        return vouchers
    
    def deactivate_voucher(self, code):
        """Deactivate a voucher"""
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("UPDATE vouchers SET status='deactivated' WHERE code=?", (code,))
        conn.commit()
        conn.close()
        return True

# Command-line interface
if __name__ == '__main__':
    import sys
    vs = VoucherSystem()
    
    if len(sys.argv) < 2:
        print("🎫 Imperial Voucher System")
        print("==========================")
        print("Commands:")
        print("  python voucher_system.py create [value] [notes]  - Create single voucher")
        print("  python voucher_system.py batch [count] [value]   - Create batch of vouchers")
        print("  python voucher_system.py list                     - List active vouchers")
        print("  python voucher_system.py stats                    - Show statistics")
        print("  python voucher_system.py validate [CODE]          - Check voucher")
        print("  python voucher_system.py use [CODE]               - Use voucher")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == 'create':
        value = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        notes = sys.argv[3] if len(sys.argv) > 3 else ''
        code = vs.create_voucher(value, notes=notes)
        print(f"✅ Voucher created: {code}")
        print(f"   Value: R{value}")
        print(f"   Valid for 30 days")
    
    elif cmd == 'batch':
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        value = int(sys.argv[3]) if len(sys.argv) > 3 else 20
        codes = vs.create_batch(count, value)
        print(f"✅ Created {len(codes)} vouchers:")
        for i, code in enumerate(codes, 1):
            print(f"  {i}. {code}")
    
    elif cmd == 'list':
        vouchers = vs.list_active()
        print(f"📋 Active Vouchers ({len(vouchers)}):")
        print("="*60)
        for v in vouchers:
            code, value, created, expires, used, max_uses = v
            print(f"  {code} | R{value} | Used: {used}/{max_uses} | Expires: {expires[:10]}")
    
    elif cmd == 'stats':
        stats = vs.get_stats()
        print("📊 Voucher Statistics")
        print("="*40)
        print(f"Total Vouchers:  {stats['total_vouchers']}")
        print(f"Active:          {stats['active']}")
        print(f"Used:            {stats['used']}")
        print(f"Revenue (ZAR):   R{stats['revenue_zar']}")
        print(f"Weekly Uses:     {stats['weekly_uses']}")
    
    elif cmd == 'validate':
        code = sys.argv[2] if len(sys.argv) > 2 else ''
        result = vs.validate_voucher(code)
        if result['valid']:
            print(f"✅ Voucher {code} is valid")
            print(f"   Value: R{result['value']}")
            print(f"   Remaining uses: {result['remaining_uses']}")
        else:
            print(f"❌ Voucher invalid: {result['reason']}")
    
    elif cmd == 'use':
        code = sys.argv[2] if len(sys.argv) > 2 else ''
        result = vs.use_voucher(code)
        if result.get('success'):
            print(f"✅ Voucher activated! You have {result['minutes']} minutes of AI access.")
        else:
            print(f"❌ Failed: {result.get('reason', 'Unknown error')}")
    
    else:
        print(f"Unknown command: {cmd}")
