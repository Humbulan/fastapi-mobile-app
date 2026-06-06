import smtplib
from email.mime.text import MIMEText
import sys

# PURE CLEAN DATA - NO EMOJIS ALLOWED
SENDER = "humbuskim@gmail.com"
RECEIVER = "humbuskim@gmail.com"
# We will pass the password as the first argument to keep it clean
PWD = sys.argv[1] 

def send_clean():
    subject = "INDUSTRIAL UPDATE: Humbu AI Platform"
    body = "Dear Sydney,\n\nInfrastructure: 48/48 Ports Verified\nValuation: R1.8 Billion\nStatus: PERMANENTLY SATISFIED\n\nRegards,\nHumbulani Mudau"
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER
    msg['To'] = RECEIVER

    try:
        print("Connecting...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        print("Logging in...")
        server.login(SENDER, PWD)
        print("Sending...")
        server.send_message(msg)
        server.quit()
        print("✅ SUCCESS: Test email sent to Humbuskim@gmail.com")
    except Exception as e:
        print(f"❌ FAILED: {e}")

if __name__ == "__main__":
    send_clean()
