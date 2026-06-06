#!/data/data/com.termux/files/usr/bin/python

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys

def create_sample_data(hours=24):
    """Create sample valuation data for analysis"""
    base_time = datetime.now()
    data = []
    
    for i in range(hours):
        # Add some variation to make it interesting
        variation = np.random.normal(0, 0.05) * 1.8e9  # 5% variation
        value = 1.806e9 + variation
        
        data.append({
            'timestamp': base_time - timedelta(hours=i),
            'valuation': value,
            'valuation_billions': value / 1e9,
            'status': 'SYNCED',
            'component': 'Imperial Omega Accounting'
        })
    
    return pd.DataFrame(data)

def analyze_valuations(df):
    """Perform comprehensive analysis"""
    
    print("=" * 60)
    print("🏛️  IMPERIAL VALUATION ANALYSIS")
    print("=" * 60)
    
    # Basic stats
    print("\n📊 BASIC STATISTICS:")
    print(f"   Records: {len(df)}")
    print(f"   Period:  {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"   Total:   R{df['valuation'].sum():,.0f}")
    print(f"   Mean:    R{df['valuation'].mean():,.0f}")
    print(f"   Median:  R{df['valuation'].median():,.0f}")
    print(f"   Std Dev: R{df['valuation'].std():,.0f}")
    print(f"   Min:     R{df['valuation'].min():,.0f}")
    print(f"   Max:     R{df['valuation'].max():,.0f}")
    
    # Time-based analysis
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    hourly_stats = df.groupby('hour')['valuation'].agg(['mean', 'min', 'max'])
    
    print("\n🕐 HOURLY AVERAGES:")
    print(hourly_stats.round(0).to_string())
    
    # Trend analysis
    df['rolling_avg'] = df['valuation'].rolling(window=6).mean()
    df['pct_change'] = df['valuation'].pct_change() * 100
    
    print("\n📈 TRENDS:")
    print(f"   Average change: {df['pct_change'].mean():.2f}%")
    print(f"   Volatility: {df['pct_change'].std():.2f}%")
    
    # Create portfolio view
    print("\n💼 PORTFOLIO ALLOCATION:")
    portfolio = pd.DataFrame({
        'asset': ['Omega Accounting', 'Imperial Core', 'Reserve Fund', 'Growth Assets'],
        'allocation': [0.58, 0.27, 0.10, 0.05],
        'value': [
            df['valuation'].mean() * 0.58,
            df['valuation'].mean() * 0.27,
            df['valuation'].mean() * 0.10,
            df['valuation'].mean() * 0.05
        ]
    })
    portfolio['value'] = portfolio['value'].round(0)
    print(portfolio.to_string(index=False))
    
    return df

if __name__ == "__main__":
    # Create sample data
    df = create_sample_data(48)  # 48 hours of data
    df = analyze_valuations(df)
    
    # Save to CSV for later analysis
    df.to_csv('valuation_history.csv', index=False)
    print("\n💾 Data saved to valuation_history.csv")
    
    # If you want interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        print("\n🔍 Interactive mode - variables available:")
        print("   df - main dataframe")
        print("   df.describe() - statistics")
        print("   df.plot() - visualization (if matplotlib installed)")
        
        # Drop into interactive mode
        import code
        code.interact(local=locals())
