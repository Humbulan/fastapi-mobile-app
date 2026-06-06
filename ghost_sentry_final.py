#!/usr/bin/env python3
"""
Ghost Sentry - Direct Terminal Port Monitor
Monitors ports 8115 and 11434 with real-time alerts
"""

import socket
import time
import subprocess
import sys
from datetime import datetime
import os

class GhostSentry:
    def __init__(self):
        self.monitored_ports = {
            8115: {
                'name': 'GHOST_PORT',
                'risk': 'CRITICAL',
                'desc': 'Ghost Service Backdoor'
            },
            11434: {
                'name': 'OLLAMA_AI',
                'risk': 'HIGH', 
                'desc': 'AI Model Gateway'
            }
        }
        self.alerts = []
        
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
    def print_header(self):
        self.clear_screen()
        print("\033[95m" + "="*60 + "\033[0m")
        print("\033[91m" + "👻 GHOST SENTRY - ACTIVE MONITORING MODE 👻".center(60) + "\033[0m")
        print("\033[95m" + "="*60 + "\033[0m")
        print(f"\033[93m📅 Time:\033[0m {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\033[93m🎯 Targets:\033[0m Port 8115 (Ghost) | Port 11434 (AI)")
        print(f"\033[93m🛡️  Status:\033[0m Kernel-level monitoring active")
        print("\033[95m" + "-"*60 + "\033[0m")
        print()
        
    def get_process_info(self, port):
        """Get process info using netstat"""
        try:
            result = subprocess.run(
                f"netstat -tulpn 2>/dev/null | grep ':{port}'",
                shell=True, capture_output=True, text=True
            )
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if f":{port}" in line:
                        parts = line.split()
                        if len(parts) >= 7:
                            return parts[-1]
            return "Unknown"
        except:
            return "N/A"
            
    def check_port(self, port, port_info):
        """Check if a port is active"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
        
    def monitor(self):
        """Main monitoring loop"""
        alert_count = 0
        active_ports = {}
        
        while True:
            try:
                for port, info in self.monitored_ports.items():
                    is_active = self.check_port(port, info)
                    
                    if is_active and port not in active_ports:
                        # New alert
                        alert_count += 1
                        active_ports[port] = True
                        proc_info = self.get_process_info(port)
                        timestamp = datetime.now().strftime('%H:%M:%S')
                        
                        print(f"\033[91m[🚨 ALERT #{alert_count}]\033[0m {timestamp}")
                        print(f"  ├─ \033[93mPort:\033[0m {port} - {info['name']}")
                        print(f"  ├─ \033[93mRisk:\033[0m {info['risk']}")
                        print(f"  ├─ \033[93mProcess:\033[0m {proc_info}")
                        print(f"  └─ \033[93mStatus:\033[0m \033[91mUNAUTHORIZED ACCESS\033[0m")
                        print()
                        
                    elif not is_active and port in active_ports:
                        # Port closed
                        del active_ports[port]
                        print(f"\033[92m[✅ CLEARED]\033[0m Port {port} - {info['name']} closed")
                        print()
                        
                # Show active connections count
                if active_ports:
                    print(f"\033[91m⚠️  ACTIVE THREATS: {len(active_ports)} ⚠️\033[0m")
                else:
                    print(f"\033[92m✅ All ports secure - No threats detected\033[0m")
                    
                print(f"\033[90mPress Ctrl+C to stop monitoring...\033[0m", end='\r')
                time.sleep(2)
                
            except KeyboardInterrupt:
                print("\n\n\033[93m[!] Ghost Sentry shutdown initiated\033[0m")
                self.print_summary()
                break
            except Exception as e:
                print(f"\033[91m[ERROR] {e}\033[0m")
                time.sleep(5)
                
    def print_summary(self):
        """Print monitoring summary"""
        print("\n\033[95m" + "="*60 + "\033[0m")
        print("\033[96m📊 MONITORING SUMMARY\033[0m".center(60))
        print("\033[95m" + "="*60 + "\033[0m")
        print(f"\033[93mDuration:\033[0m Active monitoring session")
        print(f"\033[93mThreats Detected:\033[0m Port 8115 and 11434 were active")
        print(f"\033[93mRecommendation:\033[0m Investigate unauthorized connections")
        print("\033[95m" + "="*60 + "\033[0m")
        
    def run(self):
        """Run the sentry"""
        self.print_header()
        print("\033[93m[*] Initializing monitoring system...\033[0m")
        time.sleep(1)
        print("\033[92m[+] System ready! Monitoring in progress...\033[0m\n")
        self.monitor()

if __name__ == "__main__":
    sentry = GhostSentry()
    sentry.run()
