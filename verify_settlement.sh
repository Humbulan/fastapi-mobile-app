#!/bin/bash
# Verify R879k settlement status

REFERENCE="IMP-FINAL-1772824281"
ACCOUNT="1717073040"

echo "🏛️ SOVEREIGN SETTLEMENT VERIFICATION - $(date)"
echo "=========================================="
echo ""

# Check local ledger
echo "📊 LOCAL LEDGER STATUS:"
sqlite3 ~/imperial_network/instance/imperial.db "SELECT status, amount, reference, datetime(created_at, 'localtime') FROM payment WHERE reference='$REFERENCE';"

echo ""
echo "🌍 BINDURA GATEWAY STATUS:"
curl -s http://localhost:8102/api/payments/status | grep -E "status|gateway_status|timestamp"

echo ""
echo "📜 SOVEREIGN LOG ENTRY:"
grep "$REFERENCE" ~/imperial_network/logs/sovereign.log

echo ""
echo "🔐 AUTH CODE: ORCID-0009-0000-9572-4535"
echo "=========================================="
