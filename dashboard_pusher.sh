#!/bin/bash
while true; do
    VALUATION=$(curl -s "http://localhost:9091/api/v1/query?query=imperial_valuation" | jq -r '.data.result[0].value[1]')
    GOLD=$(curl -s "http://localhost:9091/api/v1/query?query=imperial_gold_price" | jq -r '.data.result[0].value[1]')
    WEALTH=$(curl -s "http://localhost:9091/api/v1/query?query=imperial_wealth_gain" | jq -r '.data.result[0].value[1]')
    ENERGY=$(curl -s "http://localhost:9091/api/v1/query?query=imperial_energy_flow" | jq -r '.data.result[0].value[1]')
    GRID=$(curl -s "http://localhost:9091/api/v1/query?query=imperial_grid_status" | jq -r '.data.result[0].value[1]')
    PROGRESS=$(curl -s "http://localhost:9091/api/v1/query?query=imperial_progress" | jq -r '.data.result[0].value[1]')
    LITHIUM=$(curl -s "http://localhost:9091/api/v1/query?query=imperial_lithium_flow" | jq -r '.data.result[0].value[1]')
    BEIRA=$(curl -s "http://localhost:9091/api/v1/query?query=imperial_beira_status" | jq -r '.data.result[0].value[1]')
    PORT=$(curl -s "http://localhost:9091/api/v1/query?query=imperial_port_status" | jq -r '.data.result[0].value[1]')

    curl -X POST -H "X-Export-Key: 9c5b30ecb25c5392e0fcb2ce24bd4c9d" \
         -H "Content-Type: application/json" \
         -d "{\"valuation\": $VALUATION, \"gold_price\": $GOLD, \"wealth_gain\": $WEALTH, \"energy_flow\": $ENERGY, \"grid_status\": $GRID, \"progress\": $PROGRESS, \"lithium_flow\": $LITHIUM, \"beira_status\": $BEIRA, \"port_status\": $PORT, \"timestamp\": \"$(date -Iseconds)\"}" \
         https://portal.humbu.store/update-dashboard

    sleep 60
done
