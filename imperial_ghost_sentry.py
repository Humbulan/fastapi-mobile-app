#!/usr/bin/env python3
"""
Imperial Network Ghost Sentry - Specialized for Termux/Android
Monitors your specific imperial_network services
"""

import socket
import subprocess
import time
import json
import os
from datetime import datetime
from collections import defaultdict

class ImperialGhostSentry:
    def __init__(self):
        self.monitored_ports = {
            8115: {'name': 'GHOST', 'critical': True, 'desc': 'Ghost Service Port'},
            11434: {'name': 'OLLAMA_AI', 'critical': True, 'desc': 'AI Model Gateway'},
            8118: {'name': 'AI_PROXY', 'critical': False, 'desc': 'AI Proxy Gateway'},
            8094: {'name': 'SKY_WATCHER', 'critical': False, 'desc': 'Intel Redirect'},
            8105: {'name': 'SENTINEL', 'critical': False, 'desc': 'War Sentinel'},
        }
        self.service_map = self.load_service_map()
        self.alerts = []
        
    def load_service_map(self):
        """Load known services from your environment"""
        services = {}
        try:
            # Parse the dawn report output
            result = subprocess.run(
                "ps aux | grep python | grep -E 'imperial_network|ghost|ollama' | grep -v grep",
                shell=True, capture_output=True, text=True
            )
            for line in result.stdout.split('\n'):
                if line.strip():
                    parts = line.split()
                    if len(parts) > 10:
                        pid = parts[1]
                        cmd = ' '.join(parts[10:])
                        services[pid] = cmd
        except:
            pass
        return services
    
    def get_process_by_port(self, port):
        """Get process using a specific port"""
        try:
            # Try netstat first
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
                            proc = parts[-1]
                            # Try to get full command
                            pid = proc.split('/')[0] if '/' in proc else proc
                            if pid.isdigit() and pid in self.service_map:
                                return f"{proc} ({self.service_map[pid][:50]})"
                            return proc
            return "Unknown (check manually)"
        except:
            return "Permission denied (run with root?)"
    
    def check_port_status(self, port):
        """Check if port is listening"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            return result == 0
        except:
            return False
    
    def run_war_sentinel_check(self):
        """Execute War Sentinel check"""
        try:
            if os.path.exists('dawn_report_enhanced.sh'):
                result = subprocess.run(
                    'bash dawn_report_enhanced.sh 2>/dev/null | grep -E "ONLINE|OFFLINE|TRADE|LITHIUM|GOLD"',
                    shell=True, capture_output=True, text=True, timeout=5
                )
                return result.stdout[:500]
        except:
            pass
        return "War Sentinel check unavailable"
    
    def monitor_network_connections(self):
        """Monitor network connections to/from monitored ports"""
        connections = defaultdict(list)
        try:
            # Monitor netstat connections
            result = subprocess.run(
                "netstat -an 2>/dev/null | grep -E '8115|11434|8118|8094|8105'",
                shell=True, capture_output=True, text=True
            )
            for line in result.stdout.split('\n'):
                if line.strip():
                    connections['active'].append(line.strip())
        except:
            pass
        return connections
    
    def print_header(self):
        os.system('clear')
        print("\033[95m" + "═"*70 + "\033[0m")
        print("\033[91m" + "👻 IMPERIAL NETWORK GHOST SENTRY 👻".center(70) + "\033[0m")
        print("\033[95m" + "═"*70 + "\033[0m")
        print(f"\033[93m📅 Time:\033[0m {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\033[93m🎯 Environment:\033[0m Termux/Android - Imperial Network")
        print(f"\033[93m🔍 Active Services:\033[0m {len([p for p in self.monitored_ports if self.check_port_status(p)])} detected")
        print("\033[95m" + "─"*70 + "\033[0m")
        print()
    
    def run(self):
        """Main monitoring loop"""
        self.print_header()
        print("\033[93m[*] Initializing Ghost Sentry for Imperial Network...\033[0m")
        time.sleep(1)
        
        # Check all monitored ports
        threats = []
        for port, info in self.monitored_ports.items():
            if self.check_port_status(port):
                proc = self.get_process_by_port(port)
                threats.append((port, info, proc))
        
        if threats:
            print(f"\033[91m[🚨 THREAT DETECTED]\033[0m Found {len(threats)} active monitored ports\n")
            for port, info, proc in threats:
                print(f"\033[91m  ⚠️  Port {port} - {info['name']}\033[0m")
                print(f"     └─ Process: {proc}")
                if info['critical']:
                    print(f"     └─ \033[91mCRITICAL: Unauthorized access risk\033[0m")
                print()
            
            # Show active connections
            conns = self.monitor_network_connections()
            if conns['active']:
                print("\033[93m[🔌 ACTIVE CONNECTIONS]\033[0m")
                for conn in conns['active'][:5]:
                    print(f"     └─ {conn}")
            
            # War Sentinel integration
            print("\n\033[93m[🛡️ WAR SENTINEL STATUS]\033[0m")
            sentinel_status = self.run_war_sentinel_check()
            if sentinel_status:
                print(f"     {sentinel_status[:200]}")
            
        else:
            print("\033[92m[✅ SECURE]\033[0m No monitored ports are active")
            print("\033[92m[✅ WAR SENTINEL]\033[0m All systems nominal")
        
        # Show network summary
        print("\n\033[95m" + "─"*70 + "\033[0m")
        print("\033[96m📊 IMPERIAL NETWORK STATUS\033[0m")
        
        # Check key services
        services = {
            8118: "AI Proxy Gateway",
            8094: "Sky Watcher/Intel Redirect",
            8105: "War Sentinel",
            1880: "Node-RED",
            5003: "SADC Payment Gateway"
        }
        
        for port, name in services.items():
            if self.check_port_status(port):
                print(f"\033[92m  ✅ {name}\033[0m (Port {port})")
            else:
                print(f"\033[91m  ❌ {name}\033[0m (Port {port})")
        
        print("\n\033[95m" + "═"*70 + "\033[0m")
        
        # Show recommendations
        if threats:
            print("\033[93m📋 RECOMMENDATIONS:\033[0m")
            for port, info, _ in threats:
                if port == 11434:
                    print(f"  • Port 11434 (Ollama AI) is active - Expected if AI services running")
                    print(f"    Check: ps aux | grep ollama")
                elif port == 8115:
                    print(f"  • Port 8115 (Ghost) is active - INVESTIGATE IMMEDIATELY")
                    print(f"    Run: netstat -tulpn | grep 8115")
                    print(f"    Kill: kill -9 $(lsof -t -i:8115)")
            print()
        
        # Real-time monitoring option
        print("\033[96m💡 OPTIONS:\033[0m")
        print("  1. Press Ctrl+C to exit")
        print("  2. Run continuous monitoring: python3 imperial_ghost_sentry.py --watch")
        print("  3. Check all services: bash dawn_report_enhanced.sh")
        print("\033[95m" + "═"*70 + "\033[0m")
        
        # Offer continuous monitoring if requested
        if '--watch' in sys.argv:
            print("\n\033[93m[*] Entering continuous monitoring mode...\033[0m")
            try:
                while True:
                    time.sleep(10)
                    os.system('clear')
                    self.print_header()
                    self.run()
            except KeyboardInterrupt:
                print("\n\033[93m[!] Ghost Sentry stopped\033[0m")

if __name__ == "__main__":
    import sys
    sentry = ImperialGhostSentry()
    sentry.run()
