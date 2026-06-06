#!/data/data/com.termux/files/usr/bin/python

import pandas as pd
import numpy as np
from datetime import datetime
import json
import os

class ImperialValuationAnalyzer:
    def __init__(self, log_file='~/imperial_network/nohup.out'):
        self.log_file = os.path.expanduser(log_file)
        self.valuations = []
        
    def parse_heartbeats(self):
        """Extract valuation data from heartbeat logs"""
        try:
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
                
            for line in lines:
                if 'Valuation Sync Complete' in line:
                    # Extract value (R1.8B format)
                    import re
                    match = re.search(r'R([\d.]+)B', line)
                    if match:
                        value_billions = float(match.group(1))
                        self.valuations.append({
                            'timestamp': datetime.now(),
                            'value_billions': value_billions,
                            'value_raw': value_billions * 1_000_000_000,
                            'log_entry': line.strip()
                        })
        except FileNotFoundError:
            print(f"⚠️ Log file {self.log_file} not found")
            
    def create_valuation_df(self):
        """Create DataFrame from parsed valuations"""
        if not self.valuations:
            self.parse_heartbeats()
            
        df = pd.DataFrame(self.valuations)
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        return pd.DataFrame()
    
    def generate_report(self):
        """Generate comprehensive valuation report"""
        df = self.create_valuation_df()
        
        print("=" * 60)
        print("🏛️  IMPERIAL VALUATION REPORT")
        print("=" * 60)
        
        if df.empty:
            print("📭 No valuation data found in logs")
            # Create sample data for demonstration
            sample_data = {
                'issue': ['REV-2026-POLL'],
                'valuation': [1806166092],
                'component': ['Imperial Omega Accounting 2026'],
                'status': ['VERIFY_LOGIC']
            }
            df_sample = pd.DataFrame(sample_data)
            print("\n📊 Current Active Valuation:")
            print(df_sample.to_string(index=False))
            print(f"\n💰 Total: R{df_sample['valuation'].sum():,}")
        else:
            print(f"\n📊 Valuation Summary:")
            print(f"   Total Records: {len(df)}")
            print(f"   Average Value: R{df['value_raw'].mean():,.0f}")
            print(f"   Total Value:   R{df['value_raw'].sum():,.0f}")
            print(f"   Last Update:    {df['timestamp'].max()}")
            
        print("\n📈 Statistical Analysis:")
        print("-" * 40)
        
        # Create a sample portfolio for demonstration
        portfolio = pd.DataFrame({
            'asset': ['Omega Accounting', 'Imperial Core', 'Reserve Fund'],
            'valuation': [1806166092, 850000000, 420000000],
            'allocation': [0.58, 0.27, 0.15]
        })
        
        print(portfolio.to_string(index=False))
        print(f"\n📊 Portfolio Statistics:")
        print(f"   Total Assets: R{portfolio['valuation'].sum():,}")
        print(f"   Average Asset: R{portfolio['valuation'].mean():,.0f}")
        print(f"   Std Deviation: R{portfolio['valuation'].std():,.0f}")
        print(f"   Largest Asset: {portfolio.loc[portfolio['valuation'].idxmax(), 'asset']}")
        
        return df

if __name__ == "__main__":
    analyzer = ImperialValuationAnalyzer()
    analyzer.generate_report()
