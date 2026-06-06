#!/bin/bash
echo "--- [IMPERIAL NETWORK: HARDWARE LOCK ACTIVE] ---"

# 1. HARDWARE CHECK
# We check if lsusb exists first, then check for your SanDisk (0781:5567)
if ! command -v lsusb &> /dev/null; then
    echo "❌ ERROR: usbutils not installed correctly. Run 'pkg install usbutils'."
    exit 1
fi

if ! lsusb | grep -q "0781:5567"; then
    echo "❌ CRITICAL: SanDisk Hardware Token (0781:5567) NOT DETECTED."
    echo "Check connection to Samsung A73 or USB hub."
    exit 1
fi
echo "✅ HARDWARE VERIFIED: SanDisk Key 0781:5567 Detected."

# 2. SANITIZER
echo "🧹 Sanitizing Ports: 5173, 8080, 8082, 8083, 8085"
# Note: In Termux, we use 'fuser' if available, or 'kill' by port
for port in 5173 8080 8082 8083 8085; do
    fuser -k $port/tcp 2>/dev/null
done

# 3. TUNNEL PROBE
echo "📡 Probing Samsung A73 Business API..."
if curl -s -k https://api.humbu.store/ | grep -q "200\|404\|401\|403"; then
    echo "✅ TUNNEL ACTIVE: Samsung A73 Linked."
else
    echo "⚠️ WARNING: Tunnel Offline. Check Cloudflare status."
fi

# 4. THE PARTY COMMAND (95)
echo "🎈 Executing Party Command for 95..."
# [Replace the next line with your actual 95 start command if known]
echo "Party 95 initiated via Imperial Network Director."

echo "--- [SYSTEM SECURED & OPERATIONAL] ---"
