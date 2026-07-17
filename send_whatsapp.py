#!/usr/bin/env python3
import sys, datetime
message = sys.argv[1] if len(sys.argv) > 1 else "Alert"
with open("/data/data/com.termux/files/home/imperial_network/alert.log", "a") as f:
    f.write(f"[{datetime.datetime.now()}] {message}\n")
print(f"Alert logged: {message}")
# Optionally, you can add a curl to a webhook here
