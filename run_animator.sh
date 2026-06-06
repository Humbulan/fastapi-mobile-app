#!/data/data/com.termux/files/usr/bin/bash
cd ~/imperial_network
while true; do
    echo "Starting Imperial Animator at $(date)"
    python3 imperial_animator.py
    echo "Animator crashed at $(date), restarting in 2 seconds..."
    sleep 2
done
