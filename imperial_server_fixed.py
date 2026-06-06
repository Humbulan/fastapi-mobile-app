#!/usr/bin/env python3
"""
🏛️ IMPERIAL SERVER - FIXED VERSION
Only marks vouchers as used AFTER successful AI response
"""
import sqlite3
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import random
import string
import time

app = Flask(__name__)
CORS(app)

DB_PATH = '/data/data/com.termux/files/home/imperial_network/vouchers.db'
OLLAMA_URL = 'http://localhost:11434/api/generate'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS vouchers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            value INTEGER DEFAULT 20,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP,
            expires_at TIMESTAMP,
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
            response_length INTEGER,
            success BOOLEAN,
            FOREIGN KEY (voucher_code) REFERENCES vouchers(code)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'})
    
    code = data.get('code', '').strip().upper()
    message = data.get('message', '')
    
    if not code or not message:
        return jsonify({'success': False, 'message': 'Code and message required'})
    
    # First, validate voucher without marking as used
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT id, value, status, used_count, max_uses, expires_at 
        FROM vouchers WHERE code=? AND status='active'
    """, (code,))
    result = c.fetchone()
    
    if not result:
        conn.close()
        return jsonify({'success': False, 'message': 'Invalid voucher code'})
    
    vid, value, status, used_count, max_uses, expires_at = result
    expires = datetime.fromisoformat(expires_at)
    
    if expires < datetime.now():
        conn.close()
        return jsonify({'success': False, 'message': 'Voucher expired'})
    
    if used_count >= max_uses:
        conn.close()
        return jsonify({'success': False, 'message': 'Voucher already used'})
    
    conn.close()
    
    # Now call AI
    try:
        models_to_try = ['glm-5:cloud', 'qwen:0.5b']
        ai_response = None
        model_used = None
        
        for model in models_to_try:
            try:
                r = requests.post(
                    OLLAMA_URL,
                    json={
                        'model': model,
                        'prompt': message,
                        'stream': False,
                        'options': {'temperature': 0.7, 'num_predict': 1000}
                    },
                    timeout=90
                )
                
                if r.status_code == 200:
                    data = r.json()
                    ai_response = data.get('response', '').strip()
                    model_used = model
                    
                    # Only accept non-empty responses
                    if ai_response and len(ai_response) > 10:
                        break
            except:
                continue
        
        # If we got a valid response, NOW mark voucher as used
        if ai_response and len(ai_response) > 10:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("UPDATE vouchers SET used_count = used_count + 1 WHERE code=?", (code,))
            c.execute("""
                INSERT INTO usage_log (voucher_code, timestamp, session_minutes, ip_address, response_length, success)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (code, datetime.now().isoformat(), 30, request.remote_addr, len(ai_response), True))
            conn.commit()
            conn.close()
            
            return jsonify({'success': True, 'response': ai_response, 'model_used': model_used})
        else:
            # Log failed attempt without using voucher
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("""
                INSERT INTO usage_log (voucher_code, timestamp, session_minutes, ip_address, response_length, success)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (code, datetime.now().isoformat(), 0, request.remote_addr, 0, False))
            conn.commit()
            conn.close()
            
            return jsonify({
                'success': False,
                'message': 'AI temporarily unavailable. Your voucher was NOT used. Please try again.'
            })
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'AI error: {str(e)}'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM vouchers")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM vouchers WHERE used_count < max_uses")
    active = c.fetchone()[0]
    c.execute("SELECT SUM(used_count) FROM vouchers")
    used = c.fetchone()[0] or 0
    c.execute("SELECT SUM(value) FROM vouchers WHERE used_count > 0")
    revenue = c.fetchone()[0] or 0
    conn.close()
    return jsonify({
        'total_vouchers': total,
        'active': active,
        'used': used,
        'revenue_zar': revenue,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏛️ IMPERIAL SERVER - FIXED VERSION")
    print("="*60)
    print("✅ Vouchers only marked used AFTER valid AI response")
    print("🚀 Server running on port 8098")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
