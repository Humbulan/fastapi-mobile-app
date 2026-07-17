import os
log_path = os.path.expanduser('~/imperial_network/logs/encryption_service.log')
if os.path.exists(log_path):
    with open(log_path, 'r') as f:
        content = f.read()
        if 'GCM_ENCRYPT_SUCCESS' in content:
            print("✅ ENCRYPTION: AES-256-GCM verified.")
        else:
            print("⚠️ ENCRYPTION: GCM tag not found in recent logs.")
else:
    print("❌ ERROR: Encryption log file not found.")
