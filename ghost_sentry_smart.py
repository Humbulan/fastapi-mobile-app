#!/usr/bin/env python3
"""
Ghost Sentry - Smart Self-Aware Monitor
Ignores its own connections and detects real threats
"""

import socket
import time
import subprocess
import os
import sys
from datetime import datetime

class SmartGhostSentry:
    def __init__(self):
        self.monitored_ports = {
            8115: {'name': 'GHOST_PORT', 'risk': 'CRITICAL', 'desc': 'Ghost Service Backdoor'},
            11434: {'name': 'OLLAMA_AI', 'risk': 'HIGH', 'desc': 'AI Model Gateway'}
        }
        self.my_pid = os.getpid()
        self.my_process = f"python3.*ghost_sentry"
        self.alerts = []
        
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
    def print_header(self):
        self.clear_screen()
        print("\033[95m" + "="*70 + "\033[0m")
        print("\033[91m" + "👻 SMART GHOST SENTRY - SELF-AWARE MONITORING MODE 👻".center(70) + "\033[0m")
        print("\033[95m" + "="*70 + "\033[0m")
        print(f"\033[93m📅 Time:\033[0m {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\033[93m🔍 Monitor PID:\033[0m {self.my_pid} (Self-aware)")
        print(f"\033[93m🎯 Targets:\033[0m Port 8115 (Ghost) | Port 11434 (AI)")
        print(f"\033[93m🛡️  Status:\033[0m Filtering self-connections")
        print("\033[95m" + "-"*70 + "\033[0m")
        print()
        
    def get_process_info(self, port):
        """Get detailed process info using multiple methods"""
        try:
            # Method 1: Try lsof (if available)
            result = subprocess.run(
                f"lsof -i :{port} 2>/dev/null | grep LISTEN",
                shell=True, capture_output=True, text=True
            )
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 2:
                        return f"PID {parts[1]}: {parts[0]}"
            
            # Method 2: Try netstat
            result = subprocess.run(
                f"ss -tulpn 2>/dev/null | grep ':{port}' || netstat -tulpn 2>/dev/null | grep ':{port}'",
                shell=True, capture_output=True, text=True
            )
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if f":{port}" in line:
                        # Extract PID if available
                        import re
                        pid_match = re.search(r'pid[= ](\d+)', line)
                        if pid_match:
                            pid = pid_match.group(1)
                            # Get process name
                            proc_result = subprocess.run(
                                f"ps -p {pid} -o comm= 2>/dev/null",
                                shell=True, capture_output=True, text=True
                            )
                            proc_name = proc_result.stdout.strip() if proc_result.stdout else "Unknown"
                            return f"PID {pid}: {proc_name}"
            return "Unknown"
        except Exception as e:
            return f"N/A"
            
    def is_self_connection(self, port, process_info):
        """Check if the connection is from this monitoring script"""
        # Check if process info contains our PID
        if str(self.my_pid) in process_info:
            return True
        # Check if it's a python ghost script
        if "python" in process_info.lower() and "ghost" in process_info.lower():
            return True
        return False
        
    def check_port(self, port):
        """Check if a port is active"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
        
    def get_detailed_analysis(self):
        """Get comprehensive port analysis"""
        analysis = []
        
        # Check each port
        for port in self.monitored_ports:
            try:
                # Check for listening services
                result = subprocess.run(
                    f"ss -tuln 2>/dev/null | grep ':{port} '",
                    shell=True, capture_output=True, text=True
                )
                if result.stdout:
                    analysis.append(f"Port {port}: Service is LISTENING")
                    
                # Count established connections
                result = subprocess.run(
                    f"ss -tun 2>/dev/null | grep ':{port} ' | wc -l",
                    shell=True, capture_output=True, text=True
                )
                conn_count = result.stdout.strip()
                if conn_count and int(conn_count) > 0:
                    analysis.append(f"Port {port}: {conn_count} active connection(s)")
                    
            except:
                pass
                
        return analysis
        
    def monitor(self):
        """Main monitoring loop with self-awareness"""
        threat_count = 0
        active_threats = {}
        
        print("\033[93m[*] Initializing smart monitoring system...\033[0m")
        time.sleep(1)
        print("\033[92m[+] Self-aware mode active! Filtering own connections...\033[0m\n")
        
        # Do initial analysis
        analysis = self.get_detailed_analysis()
        if analysis:
            print("\033[96m📊 Initial Port Analysis:\033[0m")
            for item in analysis:
                print(f"   {item}")
            print()
        
        while True:
            try:
                current_threats = []
                
                for port, info in self.monitored_ports.items():
                    is_active = self.check_port(port)
                    
                    if is_active:
                        proc_info = self.get_process_info(port)
                        is_self = self.is_self_connection(port, proc_info)
                        
                        if not is_self:
                            # This is a real threat
                            if port not in active_threats:
                                threat_count += 1
                                timestamp = datetime.now().strftime('%H:%M:%S')
                                
                                print(f"\033[91m[🚨 REAL THREAT #{threat_count}]\033[0m {timestamp}")
                                print(f"  ├─ \033[93mPort:\033[0m {port} - {info['name']}")
                                print(f"  ├─ \033[93mRisk Level:\033[0m {info['risk']}")
                                print(f"  ├─ \033[93mProcess:\033[0m {proc_info}")
                                print(f"  ├─ \033[93mSource:\033[0m EXTERNAL/UNAUTHORIZED")
                                print(f"  └─ \033[93mAction:\033[0m \033[91mIMMEDIATE INVESTIGATION REQUIRED\033[0m")
                                print()
                                active_threats[port] = True
                                current_threats.append(port)
                            else:
                                current_threats.append(port)
                        else:
                            # Self-connection - ignore
                            if port in active_threats:
                                del active_threats[port]
                    else:
                        if port in active_threats:
                            del active_threats[port]
                            print(f"\033[92m[✅ THREAT CLEARED]\033[0m Port {port} - {self.monitored_ports[port]['name']} closed")
                            print()
                
                # Display status
                if current_threats:
                    print(f"\033[91m⚠️  REAL THREATS ACTIVE: {len(current_threats)} ⚠️\033[0m")
                    print(f"\033[93m   Affected ports: {', '.join(str(p) for p in current_threats)}\033[0m")
                else:
                    print(f"\033[92m✅ SECURE - No external threats detected\033[0m")
                    print(f"\033[90m   (Self-connections are being ignored)\033[0m")
                    
                print(f"\033[90mPress Ctrl+C to stop monitoring...\033[0m", end='\r')
                time.sleep(3)
                
            except KeyboardInterrupt:
                print("\n\n\033[93m[!] Ghost Sentry shutdown initiated\033[0m")
                self.print_summary(threat_count, active_threats)
                break
            except Exception as e:
                print(f"\033[91m[ERROR] {e}\033[0m")
                time.sleep(5)
                
    def print_summary(self, threat_count, active_threats):
        """Print monitoring summary"""
        print("\n\033[95m" + "="*70 + "\033[0m")
        print("\033[96m📊 MONITORING SUMMARY\033[0m".center(70))
        print("\033[95m" + "="*70 + "\033[0m")
        print(f"\033[93mMonitor PID:\033[0m {self.my_pid}")
        print(f"\033[93mReal Threats Detected:\033[0m {threat_count}")
        print(f"\033[93mSelf-Connections Filtered:\033[0m All monitoring services ignored")
        
        if active_threats:
            print(f"\033[91m⚠️  Current Active Threats:\033[0m")
            for port in active_threats:
                print(f"   • Port {port}: {self.monitored_ports[port]['name']} - {self.monitored_ports[port]['risk']} RISK")
        else:
            print(f"\033[92m✅ All clear - No real threats detected\033[0m")
            
        print(f"\033[93mRecommendation:\033[0m Continue monitoring for unauthorized access")
        print("\033[95m" + "="*70 + "\033[0m")
        
    def run(self):
        """Run the smart sentry"""
        self.print_header()
        self.monitor()

if __name__ == "__main__":
    sentry = SmartGhostSentry()
    sentry.run()
