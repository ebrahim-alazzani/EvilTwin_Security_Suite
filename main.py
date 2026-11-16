#!/usr/bin/env python3
"""
=============================================================================
 EvilTwin Security Suite - Professional CLI Entry Point (English Edition)
 Developed for Educational Research, Wireless Threat Analysis & Evil Twin Defense.
 Consolidated and upgraded from historical student project versions.
=============================================================================
"""

import sys
import os
import time
import socket
import platform

# Ensure local core package is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.attacker import EvilTwinServer, get_banner
from core.detector import EvilTwinDetector

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def display_header():
    print(get_banner())
    print("=" * 75)
    print("  EvilTwin Security Suite | Wireless Threat Simulation & Defense Tool")
    print("  Dedicated for Educational Research & Wi-Fi Rogue AP Detection")
    print("=" * 75)

def option_attacker():
    clear_screen()
    print("\n--- [1] Launch Attacker Simulation Server (Rogue AP Simulator) ---")
    port_input = input("Enter server port (Default 22222): ").strip()
    port = int(port_input) if port_input.isdigit() else 22222
    server = EvilTwinServer(port=port)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
    input("\nPress Enter to return to main menu...")

def option_detector():
    clear_screen()
    print("\n--- [2] Launch Evil Twin Network Detector & Defender ---")
    host_input = input("Enter target simulation host (Default 127.0.0.1): ").strip()
    port_input = input("Enter target server port (Default 22222): ").strip()
    
    host = host_input if host_input else '127.0.0.1'
    port = int(port_input) if port_input.isdigit() else 22222
    
    detector = EvilTwinDetector(target_host=host, target_port=port)
    detector.run_scan_and_inspect()
    input("\nPress Enter to return to main menu...")

def option_network_audit():
    clear_screen()
    print("\n--- [3] Network Interfaces & System Telemetry Audit ---")
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "127.0.0.1"

    print(f"[*] Hostname: {hostname}")
    print(f"[*] Primary Local IP: {local_ip}")
    print(f"[*] Operating System: {platform.system()} {platform.release()} ({platform.machine()})")

    try:
        import psutil
        print("\n[+] Detected Network Interfaces:")
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        for iface, addr_list in addrs.items():
            stat = stats.get(iface)
            status_str = "CONNECTED [UP]" if (stat and stat.isup) else "DISCONNECTED [DOWN]"
            speed = f"{stat.speed}Mbps" if (stat and stat.speed > 0) else "N/A"
            print(f"\n  * Adapter: {iface} [{status_str} | Speed: {speed}]")
            for a in addr_list:
                family = "IPv4" if a.family == socket.AF_INET else ("MAC" if hasattr(psutil, 'AF_LINK') and a.family == psutil.AF_LINK else str(a.family))
                print(f"    - {family}: {a.address}")
    except ImportError:
        print("[!] 'psutil' library is not available for full adapter inspection.")

    input("\nPress Enter to return to main menu...")

def option_view_logs():
    clear_screen()
    print("\n--- [4] View Captured Connection Logs (Logs Viewer) ---")
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    if not os.path.exists(log_dir) or not os.listdir(log_dir):
        print("[-] No session logs captured yet.")
    else:
        log_files = [f for f in os.listdir(log_dir) if f.endswith('.log') or f.endswith('.txt')]
        print(f"[+] Found {len(log_files)} log file(s):\n")
        for idx, lf in enumerate(log_files, 1):
            fp = os.path.join(log_dir, lf)
            print(f"  {idx}. {lf} ({os.path.getsize(fp)} bytes)")
        
        choice = input("\nSelect log number to inspect (or press Enter to return): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(log_files):
            chosen = log_files[int(choice) - 1]
            print(f"\n=== Log Content: {chosen} ===")
            with open(os.path.join(log_dir, chosen), 'r', encoding='utf-8', errors='ignore') as f:
                print(f.read())
            print("=" * 55)

    input("\nPress Enter to return to main menu...")

def option_docs():
    clear_screen()
    print("\n--- [5] Educational Guide & Attack Theoretical Concepts ---")
    print("""
1. What is an Evil Twin Attack?
   An Evil Twin is a rogue wireless access point (AP) that masquerades as a legitimate,
   trusted network by beaconing the exact same SSID (network name).

2. How Victims Are Trapped:
   Devices automatically associate with the access point emitting the strongest signal.
   Attackers often transmit 802.11 Deauthentication packets to forcibly disconnect clients
   from the genuine router, forcing them to re-associate with the Rogue Evil Twin AP.

3. Man-in-the-Middle (MitM) Exploitation:
   Once the victim associates with the rogue AP, all unencrypted traffic flows through
   the attacker's interface, allowing credential harvesting and session hijacking.

4. Defense & Detection Mechanism:
   - BSSID (MAC Address) Verification: Scanning for duplicate SSIDs operating on disparate BSSIDs.
   - Signal Fingerprinting & Sequence Number Analysis.
   - Enterprise Authentication (802.1X / WPA3-Enterprise).
""")
    input("\nPress Enter to return to main menu...")

def main():
    while True:
        clear_screen()
        display_header()
        print("\n  MAIN CONTROL MENU:")
        print("  [1] Launch Attacker Simulation Server (Rogue AP)")
        print("  [2] Launch Evil Twin Network Threat Detector")
        print("  [3] Network Adapters & System Telemetry Audit")
        print("  [4] Inspect Captured Connection Session Logs")
        print("  [5] Educational Security Guide & Documentation")
        print("  [6] Exit Suite")
        print("-" * 75)

        choice = input("Select an option [1-6]: ").strip()
        if choice == '1':
            option_attacker()
        elif choice == '2':
            option_detector()
        elif choice == '3':
            option_network_audit()
        elif choice == '4':
            option_view_logs()
        elif choice == '5':
            option_docs()
        elif choice == '6':
            clear_screen()
            print("\nThank you for using EvilTwin Security Suite. Goodbye!\n")
            sys.exit(0)
        else:
            print("Invalid option. Please enter a valid number (1-6).")
            time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated.")
        sys.exit(0)
