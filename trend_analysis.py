#!/usr/bin/env python3
"""
Imperial Omega Historical Trend Analysis
Generates reports and visualizations of network growth
"""

import sqlite3
import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import os
import numpy as np

class ImperialTrendAnalyzer:
    def __init__(self):
        self.db_path = os.path.expanduser('~/imperial_network/alerts.db')
        self.output_dir = os.path.expanduser('~/humbu_community_nexus/trends')
        os.makedirs(self.output_dir, exist_ok=True)
        
    def get_historical_data(self, days=30):
        """Fetch historical metrics from database"""
        conn = sqlite3.connect(self.db_path)
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        
        query = f"""
        SELECT timestamp, valuation, villages, lithium_price
        FROM metrics
        WHERE timestamp >= '{cutoff}'
        ORDER BY timestamp
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
        return df
    
    def generate_valuation_chart(self):
        """Generate valuation growth chart"""
        df = self.get_historical_data(90)  # Last 90 days
        
        if df.empty:
            print("⚠️ No historical data available yet")
            return None
            
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['valuation'], 'g-', linewidth=2, label='Valuation (RB)')
        plt.axhline(y=500, color='gold', linestyle='--', linewidth=2, label='Target: R500B')
        
        # Add trend line
        z = np.polyfit(range(len(df)), df['valuation'], 1)
        p = np.poly1d(z)
        plt.plot(df.index, p(range(len(df))), 'r--', alpha=0.5, label='Trend Line')
        
        plt.title('🏛️ Imperial Omega Valuation Growth', fontsize=16, fontweight='bold')
        plt.xlabel('Date')
        plt.ylabel('Valuation (Billion Rand)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        chart_path = os.path.join(self.output_dir, 'valuation_trend.png')
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        return chart_path
    
    def generate_growth_metrics(self):
        """Calculate and return growth metrics"""
        df = self.get_historical_data(30)
        
        if df.empty or len(df) < 2:
            return {
                'daily_growth': 0,
                'weekly_growth': 0,
                'monthly_growth': 0,
                'projected_days': 250,
                'current_valuation': 269.9
            }
        
        latest = df.iloc[-1]['valuation']
        oldest = df.iloc[0]['valuation']
        days = (df.index[-1] - df.index[0]).days
        
        if days > 0:
            daily_growth = (latest - oldest) / days
            weekly_growth = daily_growth * 7
            monthly_growth = daily_growth * 30
        else:
            daily_growth = weekly_growth = monthly_growth = 0
        
        # Project days to target
        if daily_growth > 0:
            days_to_target = (500 - latest) / daily_growth
        else:
            days_to_target = 999
            
        return {
            'daily_growth': daily_growth,
            'weekly_growth': weekly_growth,
            'monthly_growth': monthly_growth,
            'projected_days': int(days_to_target),
            'current_valuation': latest,
            'total_days_tracked': days
        }
    
    def generate_html_report(self):
        """Generate comprehensive HTML trend report"""
        metrics = self.generate_growth_metrics()
        chart_path = self.generate_valuation_chart()
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Imperial Omega Trend Analysis</title>
            <style>
                body {{ background: #0a0a0f; color: #00ff00; font-family: monospace; padding: 40px; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: #1a1a2e; border: 1px solid #00ff00; border-radius: 12px; padding: 30px; }}
                h1 {{ color: #ffd700; text-align: center; }}
                .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 30px 0; }}
                .card {{ background: #0f0f1a; padding: 20px; border-left: 4px solid #00ff00; border-radius: 8px; }}
                .value {{ font-size: 2em; font-weight: bold; color: #ffd700; }}
                .trend-up {{ color: #00ff00; }}
                .chart {{ margin: 30px 0; text-align: center; }}
                img {{ max-width: 100%; border: 1px solid #00ff00; border-radius: 8px; }}
                .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #00ff00; font-size: 0.8em; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏛️ IMPERIAL OMEGA: TREND ANALYSIS</h1>
                <p style="text-align: center;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                
                <div class="metrics-grid">
                    <div class="card">
                        <h3>📈 Growth Rates</h3>
                        <div>Daily Growth: <span class="value">{metrics['daily_growth']:.2f} RB/day</span></div>
                        <div>Weekly Growth: <span class="value">{metrics['weekly_growth']:.2f} RB/week</span></div>
                        <div>Monthly Growth: <span class="value">{metrics['monthly_growth']:.2f} RB/month</span></div>
                    </div>
                    
                    <div class="card">
                        <h3>🎯 Target Projection</h3>
                        <div>Current: <span class="value">R{metrics['current_valuation']:.1f}B</span></div>
                        <div>Target: <span class="value">R500B</span></div>
                        <div>Projected: <span class="value">{metrics['projected_days']} days</span></div>
                        <div>Tracking: <span class="value">{metrics['total_days_tracked']} days</span></div>
                    </div>
                </div>
        """
        
        if chart_path and os.path.exists(chart_path):
            import base64
            with open(chart_path, 'rb') as f:
                img_data = base64.b64encode(f.read()).decode()
            html_content += f"""
                <div class="chart">
                    <h3>📊 Valuation Growth Chart</h3>
                    <img src="data:image/png;base64,{img_data}" alt="Valuation Trend">
                </div>
            """
        
        html_content += """
                <div class="footer">
                    Imperial Omega Sovereign Intelligence | Automated Trend Analysis<br>
                    Data collected from live network metrics
                </div>
            </div>
        </body>
        </html>
        """
        
        report_path = os.path.join(self.output_dir, 'trend_report.html')
        with open(report_path, 'w') as f:
            f.write(html_content)
        
        return report_path

if __name__ == "__main__":
    analyzer = ImperialTrendAnalyzer()
    report = analyzer.generate_html_report()
    print(f"✅ Trend report generated: {report}")
