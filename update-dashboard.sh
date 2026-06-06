#!/bin/bash
# Generate the Imperial Dashboard
REPORT_FILE=$(ls -t ~/humbu_community_nexus/daily_summary_*.txt | head -1)
{
  echo "<html><body style='background:#1a1a1a; color:#00ff00; font-family:monospace;'>"
  echo "<h1>🦞 Imperial Audit Dashboard</h1>"
  echo "<h3>Latest Report: $(basename $REPORT_FILE)</h3>"
  echo "<pre style='background:#000; padding:20px; border:1px solid #333;'>"
  cat "$REPORT_FILE"
  echo "</pre></body></html>"
} > ~/imperial_network/dashboard.html
