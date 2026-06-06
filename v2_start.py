from app import app, VILLAGES, TOTAL_WEALTH
import os

if __name__ == "__main__":
    print("🚀 Starting Imperial Village Admin V2...")
    print(f"💰 Wealth: R{TOTAL_WEALTH:,.2f} | 📍 Villages: 43")
    app.run(host='0.0.0.0', port=8000, debug=False)
