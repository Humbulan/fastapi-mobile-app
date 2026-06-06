#!/bin/bash
# IMPERIAL OMEGA - STABLE SMTP DISPATCHER
SIGNATURE_FILE="/data/data/com.termux/files/home/imperial_network/SADC_Transit_Signature.json"

echo "INITIATING STABLE SMTP DISPATCH..."

python3 -c "
import smtplib, os
from email.mime.text import MIMEText
from email.utils import formataddr

def send():
    try:
        with open('$SIGNATURE_FILE', 'r') as f:
            sig = f.read()
    except:
        sig = 'Signature missing'

    sender = 'humbuskim@gmail.com'
    pwd = os.environ.get('GMAIL_APP_PASSWORD', '')
    
    subject = 'INDUSTRIAL UPDATE: Humbu AI Platform - March 2026'
    body = f'Dear Sydney,\n\nInfrastructure: 48/48 Ports Verified\nValuation: R1.8 Billion\nStatus: PERMANENTLY SATISFIED\n\nSIGNATURE:\n{sig}\n\nRegards,\nHumbulani Mudau'
    
    # Strip any potential emoji/non-ascii data
    clean_body = body.encode('ascii', 'ignore').decode('ascii')

    msg = MIMEText(clean_body)
    msg['Subject'] = subject
    msg['From'] = formataddr(('CEO | Humbu Imperial Nexus', sender))
    msg['To'] = 'humbuskim@gmail.com'

    try:
        # Use Port 587 with STARTTLS for better stability
        print('Connecting to SMTP...')
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1) # This will show us exactly where it fails
        server.starttls()
        print('Logging in...')
        server.login(sender, pwd)
        print('Sending message...')
        server.send_message(msg)
        server.quit()
        print('SUCCESS: Email delivered to Humbuskim@gmail.com')
    except Exception as e:
        print(f'FAILED: {e}')

send()
"
