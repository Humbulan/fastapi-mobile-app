#!/usr/bin/env python3
"""
Ghost Sentry - Direct Terminal Port Monitor
Monitors ports 8115 and 11434 at the system level
"""

import socket
import struct
import time
import os
import sys
from datetime import datetime
import threading
import subprocess

class GhostSentry:
    def __init__(self):
        self.monitored_ports = {8115: "GHOST_PORT", 11434: "OLLAMA_AI"}
        self.active_connections = {}
        
    def print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════╗
║           👻 GHOST SENTRY - ACTIVE 👻                ║
║     Kernel-Level Port Monitoring System              ║
║     Monitoring Ports: 8115 (Ghost), 11434 (AI)      ║
╚══════════════════════════════════════════════════════╝
        """
        print(banner)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] System initialized")
        
    def get_process_by_port(self, port):
        """Get process using a specific port"""
        try:
            # For Linux/Android/Termux
            cmd = f"netstat -tulpn 2>/dev/null | grep ':{port} '"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if f":{port}" in line:
                        parts = line.split()
                        if len(parts) >= 7:
                            return parts[-1]  # PID/Program name
            return "Unknown"
        except:
            return "N/A"
    
    def monitor_connections(self):
        """Monitor active network connections"""
        while True:
            try:
                # Check each monitored port
                for port, name in self.monitored_ports.items():
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex(('127.0.0.1', port))
                    sock.close()
                    
                    if result == 0:
                        if port not in self.active_connections or not self.active_connections[port]:
                            proc_info = self.get_process_by_port(port)
                            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            print(f"\033[91m[ALERT]\033[0m [{timestamp}] 🚨 {name} (Port {port}) ACTIVE")
                            print(f"  └─ Process: {proc_info}")
                            print(f"  └─ Status: UNAUTHORIZED ACCESS DETECTED")
                            self.active_connections[port] = True
                    else:
                        if port in self.active_connections:
                            del self.active_connections[port]
                            
                time.sleep(2)  # Check every 2 seconds
                
            except KeyboardInterrupt:
                print("\n\n[!] Ghost Sentry shutdown initiated")
                break
            except Exception as e:
                print(f"[ERROR] {e}")
                time.sleep(5)
    
    def packet_sniffer(self):
        """Simple packet capture using scapy if available"""
        try:
            from scapy.all import sniff, IP, TCP
            print("[+] Advanced packet capture enabled")
            
            def packet_callback(packet):
                if IP in packet and TCP in packet:
                    src_port = packet[TCP].sport
                    dst_port = packet[TCP].dport
                    
                    if dst_port in self.monitored_ports or src_port in self.monitored_ports:
                        port = dst_port if dst_port in self.monitored_ports else src_port
                        name = self.monitored_ports.get(port, "UNKNOWN")
                        print(f"\033[93m[PACKET]\033[0m {name} traffic detected - {packet[IP].src}:{src_port} -> {packet[IP].dst}:{dst_port}")
            
            sniff(filter="tcp port 8115 or tcp port 11434", prn=packet_callback, store=0)
        except ImportError:
            print("[!] Scapy not installed - using basic monitoring only")
        except Exception as e:
            print(f"[!] Packet capture error: {e}")
    
    def run(self):
        """Main execution"""
        self.print_banner()
        
        # Check if we should use packet capture
        use_advanced = input("\nEnable advanced packet capture? (y/N): ").lower() == 'y'
        
        if use_advanced:
            # Start packet sniffer in separate thread
            sniff_thread = threading.Thread(target=self.packet_sniffer, daemon=True)
            sniff_thread.start()
            print("[+] Advanced monitoring enabled\n")
        else:
            print("[+] Basic monitoring enabled\n")
        
        # Start connection monitoring
        print("[*] Monitoring system connections... (Press Ctrl+C to stop)\n")
        try:
            self.monitor_connections()
        except KeyboardInterrupt:
            print("\n\n[*] Ghost Sentry stopped")
            sys.exit(0)

if __name__ == "__main__":
    sentry = GhostSentry()
    sentry.run()
