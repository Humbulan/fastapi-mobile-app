#!/usr/bin/env python3
import requests, sys

def log_to_nexus(vuln, severity, port):
    url = "http://localhost:8002/log"
    payload = {
        "vulnerability": vuln,
        "severity": severity,
        "target_port": port
    }
    try:
        res = requests.post(url, json=payload)
        return res.status_code == 200
    except Exception as e:
        print(f"Exception: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) == 4:
        print(log_to_nexus(sys.argv[1], sys.argv[2], int(sys.argv[3])))
