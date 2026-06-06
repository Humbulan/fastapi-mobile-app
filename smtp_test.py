import smtplib
import os

sender = "humbuskim@gmail.com"
password = os.environ.get('GMAIL_APP_PASSWORD', '')

print(f"Testing SMTP with password length: {len(password)}")

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender, password)
    print("✅ Login successful!")
    server.quit()
except Exception as e:
    print(f"❌ Login failed: {e}")
