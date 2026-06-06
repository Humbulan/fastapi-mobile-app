#!/bin/bash
echo "📊 IMPERIAL WEEKLY SUMMARY"
echo "================================="
grep -E "Status:|Commission \(R4\):" ~/humbu_community_nexus/daily_summary_*.txt | awk -F': ' '{print $2}' | sort | uniq -c
