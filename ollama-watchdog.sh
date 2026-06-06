#!/bin/bash
# Ollama watchdog - ensures AI service stays running

while true; do
    if ! pgrep -f "ollama serve" > /dev/null; then
        echo "$(date): Ollama down - restarting" >> ~/imperial_network/logs/ollama-watchdog.log
        nohup ollama serve > ~/imperial_network/logs/ollama.log 2>&1 &
    fi
    sleep 30
done
