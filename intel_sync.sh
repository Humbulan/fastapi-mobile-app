#!/bin/bash
# Imperial Omega: Intel Vault Sync (Port 8191)
VAULT_DIR="$HOME/imperial_network/vault_8191"
SOURCE_DIR="$HOME/imperial_network"
LOG_FILE="$HOME/imperial_network/logs/intel_sync.log"

mkdir -p "$VAULT_DIR"
echo "[$(date)] Sealing Authority Documents into Vault..." >> "$LOG_FILE"

# Copying the specific verified PDFs found in the audit
cp "$SOURCE_DIR/Humbu_Business_Plan_Mar2026.pdf" "$VAULT_DIR/"
cp "$SOURCE_DIR/IMPERIAL_OMEGA_SOVEREIGN_STRATEGY_2026.pdf" "$VAULT_DIR/"
cp "$SOURCE_DIR/technical_methodology.pdf" "$VAULT_DIR/"

# Generate clean JSON array for the endpoint
FILES_JSON=$(ls "$VAULT_DIR" 2>/dev/null | jq -R . | jq -s . || echo "[]")
COUNT=$(ls -1 "$VAULT_DIR" 2>/dev/null | wc -l)

# Update the state file used by the 8191 service
echo "{\"service\": \"Intel_Files\", \"status\": \"online\", \"classification\": \"TOP SECRET\", \"total_files\": $COUNT, \"files\": $FILES_JSON, \"timestamp\": \"$(date)\"}" > ~/imperial_network/data/intel_8191.json

echo "[$(date)] Vault 8191 Secured: $COUNT files indexed." >> "$LOG_FILE"
