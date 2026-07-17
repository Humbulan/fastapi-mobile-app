#!/usr/bin/env python3
"""
SADC Payment Gateway - Cross-Border Payment Processing
Fixed version with proper transaction loading
"""

import json
import os
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import threading
import time

class SilentHTTPServer(HTTPServer):
    def server_bind(self):
        try:
            super().server_bind()
        except OSError as e:
            if e.errno == 98:
                pass
            else:
                raise

class SADCPaymentGateway:
    def __init__(self):
        self.transactions = []
        self.currencies = {
            'ZAR': {'name': 'South African Rand', 'symbol': 'R', 'rate': 1.0},
            'USD': {'name': 'US Dollar', 'symbol': '$', 'rate': 18.50},
            'EUR': {'name': 'Euro', 'symbol': '€', 'rate': 20.10},
            'GBP': {'name': 'British Pound', 'symbol': '£', 'rate': 23.40},
            'BWP': {'name': 'Botswana Pula', 'symbol': 'P', 'rate': 0.75},
            'MZN': {'name': 'Mozambican Metical', 'symbol': 'MT', 'rate': 0.29},
            'ZWL': {'name': 'Zimbabwe Gold', 'symbol': 'ZiG', 'rate': 0.55},
            'NAD': {'name': 'Namibian Dollar', 'symbol': 'N$', 'rate': 0.95},
            'LSL': {'name': 'Lesotho Loti', 'symbol': 'L', 'rate': 0.95},
            'SZL': {'name': 'Swazi Lilangeni', 'symbol': 'E', 'rate': 0.95}
        }
        self.sadc_countries = {
            'ZA': 'South Africa', 'ZW': 'Zimbabwe', 'MZ': 'Mozambique',
            'BW': 'Botswana', 'NA': 'Namibia', 'LS': 'Lesotho',
            'SZ': 'Eswatini', 'ZM': 'Zambia', 'MW': 'Malawi',
            'TZ': 'Tanzania', 'AO': 'Angola', 'CD': 'DR Congo',
            'MG': 'Madagascar', 'MU': 'Mauritius', 'SC': 'Seychelles',
            'KM': 'Comoros'
        }
        self.load_transactions()
        print(f"📊 SADC Gateway initialized: Loaded {len(self.transactions)} transactions")
        if self.transactions:
            total = sum(t.get('converted_amount', t.get('amount', 0)) for t in self.transactions)
            print(f"💰 Total Volume: R{total:,.2f}")
    
    def load_transactions(self):
        """Load existing transactions from log"""
        log_file = os.path.expanduser('~/imperial_network/logs/sadc_payments.log')
        loaded = 0
        try:
            with open(log_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        # Ensure amounts are floats
                        if 'amount' in data:
                            data['amount'] = float(data['amount'])
                        if 'converted_amount' in data:
                            data['converted_amount'] = float(data['converted_amount'])
                        self.transactions.append(data)
                        loaded += 1
                    except json.JSONDecodeError as e:
                        print(f"⚠️ Skipping line {line_num}: {e}")
                        continue
        except FileNotFoundError:
            print("📝 No existing transactions log found")
        except Exception as e:
            print(f"⚠️ Error loading transactions: {e}")
        
        print(f"📥 Loaded {loaded} transactions from log")
        return loaded
    
    def save_transaction(self, transaction):
        """Save transaction to log"""
        log_file = os.path.expanduser('~/imperial_network/logs/sadc_payments.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(json.dumps(transaction) + '\n')
        self.transactions.insert(0, transaction)
    
    def generate_transaction_id(self):
        """Generate unique transaction ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_part = secrets.token_hex(4).upper()
        return f"SADC-{timestamp}-{random_part}"
    
    def process_payment(self, payment_data):
        """Process cross-border payment"""
        # Calculate exchange rate and converted amount
        from_currency = payment_data.get('currency', 'ZAR')
        exchange_rate = self.currencies.get(from_currency, {'rate': 1.0})['rate']
        amount = float(payment_data.get('amount', 0))
        converted_amount = round(amount * exchange_rate, 2)
        
        transaction = {
            'transaction_id': self.generate_transaction_id(),
            'timestamp': datetime.now().isoformat(),
            'amount': amount,
            'currency': from_currency,
            'from_country': payment_data.get('from_country', 'ZA'),
            'to_country': payment_data.get('to_country', 'ZA'),
            'payer': payment_data.get('payer', {}),
            'payee': payment_data.get('payee', {}),
            'purpose': payment_data.get('purpose', 'General Trade'),
            'status': 'COMPLETED',
            'exchange_rate': exchange_rate,
            'sadc_corridor': self.get_sadc_corridor(
                payment_data.get('from_country', 'ZA'),
                payment_data.get('to_country', 'ZA')
            ),
            'converted_amount': converted_amount,
            'converted_currency': 'ZAR'
        }
        
        # Save transaction
        self.save_transaction(transaction)
        
        # Forward to Node-RED callback
        self.forward_to_nodered(transaction)
        
        return transaction
    
    def get_exchange_rate(self, currency):
        """Get exchange rate to ZAR"""
        return self.currencies.get(currency, {'rate': 1.0})['rate']
    
    def get_sadc_corridor(self, from_country, to_country):
        """Determine SADC trade corridor"""
        corridors = {
            ('ZA', 'ZW'): 'North-South Corridor (SA-Zim)',
            ('ZA', 'MZ'): 'Maputo Corridor',
            ('ZW', 'MZ'): 'Beira Corridor',
            ('ZA', 'BW'): 'Trans-Kalahari Corridor',
            ('NA', 'ZA'): 'Walvis Bay Corridor',
            ('ZA', 'ZM'): 'North-South Corridor (SA-Zambia)',
            ('MZ', 'ZW'): 'Beira Corridor (Moz-Zim)',
            ('BW', 'ZA'): 'Trans-Kalahari Corridor (Botswana-SA)',
            ('MZ', 'ZA'): 'Maputo Corridor (Moz-SA)'
        }
        return corridors.get((from_country, to_country), 'SADC Regional Corridor')
    
    def process_by_corridor(self, transaction):
        """Process based on corridor type"""
        corridor = transaction.get('sadc_corridor', '')
        
        if 'North-South' in corridor:
            return 'COMPLETED'
        elif 'Maputo' in corridor:
            return 'COMPLETED'
        elif 'Beira' in corridor:
            return 'COMPLETED'
        elif 'Trans-Kalahari' in corridor:
            return 'COMPLETED'
        else:
            return 'COMPLETED'
    
    def forward_to_nodered(self, transaction):
        """Forward transaction to Node-RED for dashboard display"""
        try:
            import subprocess
            subprocess.run([
                'curl', '-s', '-X', 'POST', 'http://localhost:1880/sadc/payment',
                '-H', 'Content-Type: application/json',
                '-d', json.dumps(transaction)
            ], timeout=2, capture_output=True)
        except:
            pass
    
    def get_stats(self):
        """Get payment statistics"""
        if not self.transactions:
            return {
                'total_transactions': 0,
                'total_volume': 0,
                'active_corridors': [],
                'top_currencies': [],
                'recent_transactions': []
            }
        
        # Calculate total volume from converted_amount or amount
        total_volume = 0
        for t in self.transactions:
            if 'converted_amount' in t:
                total_volume += t['converted_amount']
            else:
                total_volume += t.get('amount', 0)
        
        total_transactions = len(self.transactions)
        
        # Count by corridor
        corridors = {}
        for t in self.transactions:
            corridor = t.get('sadc_corridor', 'Unknown')
            corridors[corridor] = corridors.get(corridor, 0) + 1
        
        # Count by currency
        currencies = {}
        for t in self.transactions:
            currency = t.get('currency', 'ZAR')
            amount = t.get('converted_amount', t.get('amount', 0))
            currencies[currency] = currencies.get(currency, 0) + amount
        
        return {
            'total_transactions': total_transactions,
            'total_volume': round(total_volume, 2),
            'active_corridors': list(corridors.keys()),
            'top_currencies': sorted(currencies.items(), key=lambda x: x[1], reverse=True)[:5],
            'recent_transactions': self.transactions[:10]
        }

class SADCHandler(BaseHTTPRequestHandler):
    gateway = SADCPaymentGateway()
    
    def do_GET(self):
        if self.path == '/' or self.path == '/sadc':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            stats = self.gateway.get_stats()
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>SADC Payment Gateway</title>
                <style>
                    body {{ background: #0a0a0f; color: #00ff00; font-family: monospace; padding: 40px; }}
                    .container {{ max-width: 1200px; margin: 0 auto; background: #1a1a2e; border: 1px solid #ffd700; padding: 30px; border-radius: 12px; }}
                    h1 {{ color: #ffd700; text-align: center; }}
                    .status {{ color: #00ff00; font-weight: bold; }}
                    .stat {{ background: #0f0f1a; padding: 15px; margin: 10px 0; border-left: 4px solid #ffd700; }}
                    .value {{ font-size: 24px; font-weight: bold; color: #ffd700; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🏛️ SADC PAYMENT GATEWAY</h1>
                    <p class="status">⚡ SOVEREIGN ACTIVE ⚡</p>
                    <p>Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    
                    <div class="stat">
                        <div class="value">R{stats['total_volume']:,.2f}</div>
                        <div>Total Trade Volume</div>
                    </div>
                    
                    <div class="stat">
                        <div class="value">{stats['total_transactions']}</div>
                        <div>Total Transactions</div>
                    </div>
                    
                    <h3>📡 Available Endpoints:</h3>
                    <div class="stat">POST /sadc/payment - Process SADC Payment</div>
                    <div class="stat">GET /sadc/stats - Payment Statistics</div>
                    <div class="stat">GET /sadc/currencies - Available Currencies</div>
                    
                    <hr>
                    <p>🇿🇦 SADC Regional Integration | Cross-Border Payments | Real-Time Settlement</p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            
        elif self.path == '/sadc/stats':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            stats = self.gateway.get_stats()
            self.wfile.write(json.dumps(stats, indent=2).encode())
            
        elif self.path == '/sadc/currencies':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(self.gateway.currencies, indent=2).encode())
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/sadc/payment':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                payment_data = json.loads(post_data)
                transaction = self.gateway.process_payment(payment_data)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(transaction, indent=2).encode())
                
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] SADC: {args[0] if args else format}")

def run():
    port = 5003
    server = SilentHTTPServer(('0.0.0.0', port), SADCHandler)
    print(f"\n🏛️ SADC Payment Gateway running on port {port}")
    print(f"   Process Payment: POST http://localhost:{port}/sadc/payment")
    print(f"   Stats: GET http://localhost:{port}/sadc/stats")
    print(f"   Currencies: GET http://localhost:{port}/sadc/currencies")
    print("Press Ctrl+C to stop\n")
    server.serve_forever()

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print("\n🛑 SADC Gateway stopped")
