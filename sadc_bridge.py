#!/usr/bin/env python3
import requests, sys

def log_metric(name, value, unit, region):
    url = "http://localhost:5008/log_sadc"
    payload = {
        "metric_name": name,
        "metric_value": value,
        "unit": unit,
        "region": region
    }
    try:
        res = requests.post(url, json=payload)
        return res.status_code == 200
    except Exception:
        return False

if __name__ == "__main__":
    if len(sys.argv) == 5:
        print(log_metric(sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4]))
