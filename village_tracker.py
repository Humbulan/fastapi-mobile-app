#!/usr/bin/env python3
import json
from datetime import datetime, timedelta

# Current village data (March 2026)
CURRENT_VILLAGES = 43
TARGET_VILLAGES = 900

# Historical growth (weekly)
growth_history = [5, 8, 12, 18, 25, 32, 43]  # Last 7 weeks

# Calculate growth rates
weekly_growth_rates = []
for i in range(1, len(growth_history)):
    rate = (growth_history[i] - growth_history[i-1]) / growth_history[i-1]
    weekly_growth_rates.append(rate)

avg_weekly_rate = sum(weekly_growth_rates) / len(weekly_growth_rates)

# Projections
weeks_to_target = 0
villages = CURRENT_VILLAGES
projections = []

while villages < TARGET_WEALTH and weeks_to_target < 200:
    villages *= (1 + avg_weekly_rate)
    weeks_to_target += 1
    projections.append({
        "week": weeks_to_target,
        "villages": round(villages)
    })

print("🏘️ IMPERIAL VILLAGE EXPANSION TRACKER")
print("="*50)
print(f"Current Villages: {CURRENT_VILLAGES}")
print(f"Target: {TARGET_VILLAGES}")
print(f"Progress: {(CURRENT_VILLAGES/TARGET_VILLAGES)*100:.1f}%")
print(f"Weekly Growth Rate: {avg_weekly_rate*100:.1f}%")
print(f"Projected to target: {weeks_to_target} weeks")
print("="*50)
print("\n📅 PROJECTION TIMELINE:")
for proj in projections[:10]:  # Show first 10 weeks
    date = datetime.now() + timedelta(weeks=proj['week'])
    print(f"  Week {proj['week']} ({date.strftime('%Y-%m-%d')}): {proj['villages']} villages")
