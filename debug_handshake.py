#!/usr/bin/env python3
import requests

def debug_bridge():
    try:
        sse = requests.get("http://localhost:8002/sse", stream=True)
        print(f"Status Code: {sse.status_code}")
        for line in sse.iter_lines():
            print(f"DEBUG: Line: {line}")
            if b"sessionId=" in line:
                sid = line.split(b"sessionId=")[1].decode().split('"')[0].strip()
                print(f"FOUND SESSION ID: {sid}")
                return
        print("NO SESSION ID FOUND IN STREAM")
    except Exception as e:
        print(f"CONNECTION ERROR: {e}")

debug_bridge()
