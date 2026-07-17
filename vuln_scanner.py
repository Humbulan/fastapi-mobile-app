#!/usr/bin/env python3
import socket
import subprocess
import sys

def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

def main():
    print("[Scanner] Running basic vulnerability scan...")
    print("Checking common ports:")
    ports = [22, 80, 443, 3000, 3306, 5000, 8000, 8080, 8118, 8888, 9090, 11434]
    for port in ports:
        status = "OPEN" if check_port(port) else "closed"
        print(f"  Port {port}: {status}")
    print("\nChecking running services:")
    try:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        for line in lines:
            if "uvicorn" in line or "ollama" in line or "python" in line:
                print("  " + line.strip()[:80])
    except Exception as e:
        print("Error running ps:", e)
    print("\nScan complete.")

if __name__ == "__main__":
    main()
