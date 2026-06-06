#!/bin/bash
STORE="$HOME/.wacli_imperial"
JID="27794658481@s.whatsapp.net"

# Only send if the DB is not locked by the main sync
if [ ! -f "$STORE/LOCK" ]; then
    wacli --store "$STORE" send text --to "$JID" --message "🏛️ IMPERIAL HEARTBEAT: $(date '+%Y-%m-%d %H:%M') | Ports: 51/51 | Stack: Online" &>/dev/null
fi
