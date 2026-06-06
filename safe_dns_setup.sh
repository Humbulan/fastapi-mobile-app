#!/bin/bash
echo "🔐 IMPERIAL DNS SAFE SETUP"
echo "==========================="
echo ""
echo "STEP 1: Go to https://dash.cloudflare.com/profile/api-tokens"
echo "STEP 2: Click 'Revoke' on ALL existing tokens"
echo "STEP 3: Click 'Create Token' → 'Edit zone DNS' template"
echo "STEP 4: Select 'humbu.store' and click 'Continue to summary'"
echo "STEP 5: Copy the new token"
echo ""
read -p "Have you revoked the old tokens? (yes/no): " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
  echo "❌ Please revoke old tokens first!"
  exit 1
fi

read -s -p "Enter your NEW API token: " CF_API_TOKEN
echo ""
read -p "Enter your Zone ID (from Cloudflare dashboard): " CF_ZONE_ID

# Store securely
echo "export CF_API_TOKEN='$CF_API_TOKEN'" > ~/.cf_secure
echo "export CF_ZONE_ID='$CF_ZONE_ID'" >> ~/.cf_secure
chmod 600 ~/.cf_secure

echo "✅ Credentials stored securely in ~/.cf_secure"

# Now configure DNS
TUNNEL_ID="d512566a-7849-4442-8e07-97b74eaccc37"
TARGET="${TUNNEL_ID}.cfargotunnel.com"

echo "🔄 Configuring DNS..."

# Add root domain
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"type":"CNAME","name":"@","content":"'"$TARGET"'","ttl":1,"proxied":true}' \
  | grep -q '"success":true' && echo "✅ Root domain (humbu.store) configured" || echo "❌ Failed"

# Add www
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"type":"CNAME","name":"www","content":"'"$TARGET"'","ttl":1,"proxied":true}' \
  | grep -q '"success":true' && echo "✅ www.humbu.store configured" || echo "❌ Failed"

echo ""
echo "⏳ Waiting 30 seconds for DNS to propagate..."
sleep 30

echo ""
echo "🔍 Testing domains:"
echo "-------------------"
curl -I https://humbu.store/ 2>/dev/null | head -n1
curl -I https://www.humbu.store/ 2>/dev/null | head -n1

echo ""
echo "🏛️ IMPERIAL DNS CONFIGURATION COMPLETE"
echo "Remember to keep your API token secure!"
