#!/data/data/com.termux/files/usr/bin/bash
PIPE="/data/data/com.termux/files/usr/tmp/imperial_pipe"
STORE="$HOME/.wacli_imperial"

while true; do
    if read line < "$PIPE"; then
        TO=$(echo "$line" | cut -d'|' -f1)
        MSG=$(echo "$line" | cut -d'|' -f2)
        # Pointing to the Imperial Store here fixes the "not authenticated" error
        wacli --store "$STORE" send text --to "$TO" --message "$MSG" >> ~/imperial-broadcast.log 2>&1
    fi
done
