#!/bin/bash
# Permanent dawn-report wrapper
~/imperial_network/batch-audit.sh ~/imperial_network/manifests.txt | tee ~/humbu_community_nexus/daily_summary_$(date +%Y%m%d).txt
