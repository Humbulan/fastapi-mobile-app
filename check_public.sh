#!/bin/bash
echo "🏛️ IMPERIAL PUBLIC STATUS CHECK - $(date)"
echo "=========================================="
for domain in humbu.store www.humbu.store imperial.humbu.store files.humbu.store monitor.humbu.store secret.humbu.store api.humbu.store; do
  status=$(curl -s -o /dev/null -w "%{http_code}" https://$domain 2>/dev/null)
  echo "$domain: $status"
done
