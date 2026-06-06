#!/usr/bin/env python3
import random
import numpy as np
import json
from datetime import datetime

# Current imperial data (March 2026)
CURRENT_WEALTH = 269905206654.89
TARGET_WEALTH = 500000000000
GAP = TARGET_WEALTH - CURRENT_WEALTH

# Growth scenarios
SCENARIOS = {
    "conservative": 0.297,  # 29.7% (lithium surge rate)
    "moderate": 0.50,        # 50%
    "aggressive": 0.75       # 75%
}

def monte_carlo_simulation(scenario_rate, iterations=10000):
    """Run Monte Carlo simulation for days to target"""
    results = []
    
    for _ in range(iterations):
        # Add randomness: ±5% variance
        actual_rate = scenario_rate * random.uniform(0.95, 1.05)
        
        # Daily growth (annual rate / 365)
        daily_rate = actual_rate / 365
        
        # Calculate days needed
        days = 0
        wealth = CURRENT_WEALTH
        
        while wealth < TARGET_WEALTH and days < 2000:
            wealth *= (1 + daily_rate)
            days += 1
        
        results.append(days)
    
    return {
        "mean": np.mean(results),
        "median": np.median(results),
        "p10": np.percentile(results, 10),
        "p90": np.percentile(results, 90),
        "min": min(results),
        "max": max(results)
    }

# Run simulations
print("🏛️ IMPERIAL OMEGA - MONTE CARLO PROJECTIONS")
print("="*50)
print(f"Current Wealth: R{CURRENT_WEALTH:,.2f}")
print(f"Target: R{TARGET_WEALTH:,.2f}")
print(f"Gap: R{GAP:,.2f}")
print("="*50)

for name, rate in SCENARIOS.items():
    sim = monte_carlo_simulation(rate)
    print(f"\n📈 {name.upper()} SCENARIO ({rate*100:.1f}% annual):")
    print(f"  • Mean: {sim['mean']:.0f} days")
    print(f"  • Median: {sim['median']:.0f} days")
    print(f"  • 10th-90th percentile: {sim['p10']:.0f} - {sim['p90']:.0f} days")
    print(f"  • Range: {sim['min']:.0f} - {sim['max']:.0f} days")

print("\n✅ Based on 10,000 simulations per scenario")
