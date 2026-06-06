#!/data/data/com.termux/files/usr/bin/python

import pandas as pd
import numpy as np
from datetime import datetime
import time
import os

def check_valuations():
    """Monitor valuation data for anomalies"""
    
    if os.path.exists('valuation_history.csv'):
        df = pd.read_csv('valuation_history.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        print(f"\n{'='*50}")
        print(f"📊 IMPERIAL VALUATION MONITOR")
        print(f"{'='*50}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\n📈 Current Status:")
        print(f"   Records: {len(df)}")
        print(f"   Latest: R{df['valuation'].iloc[-1]/1e9:.3f}B")
        print(f"   Average: R{df['valuation'].mean()/1e9:.3f}B")
        print(f"   Total: R{df['valuation'].sum()/1e9:.1f}B")
        
        # Check for anomalies
        leaks = df[df['valuation'] < 1.65e9]
        if len(leaks) > 0:
            print(f"\n⚠️  WARNING: {len(leaks)} value leaks detected!")
            for _, row in leaks.iterrows():
                print(f"   • {row['timestamp']}: R{row['valuation']/1e9:.3f}B")
        else:
            print(f"\n✅ No value leaks detected")
        
        # Calculate stability
        volatility = df['valuation'].pct_change().std() * 100
        print(f"\n📊 Volatility: {volatility:.2f}%")
        
        if volatility < 5:
            print("   Status: STABLE")
        elif volatility < 10:
            print("   Status: MODERATE")
        else:
            print("   Status: VOLATILE")
            
    else:
        print("❌ No valuation history found")

if __name__ == "__main__":
    check_valuations()
