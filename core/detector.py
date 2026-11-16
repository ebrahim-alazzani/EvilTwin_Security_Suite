"""
EvilTwin Security Suite - Network Defender & Detection Module
Analyzes Wi-Fi beacons and network topology to detect Evil Twin rogue access points,
BSSID spoofing, and duplicate SSID anomalies.
"""

import socket
import ast
import platform
import os
import time

class EvilTwinDetector:
    def __init__(self, target_host='127.0.0.1', target_port=22222):
        self.target_host = target_host
        self.target_port = target_port

    def get_system_audit(self):
        audit = {
            "OS": f"{platform.system()} {platform.release()}",
            "Hostname": platform.node(),
            "Architecture": platform.machine(),
            "Python": platform.python_version()
        }
        return audit

    def analyze_networks(self, raw_network_list):
        """
        Takes list of [SSID1, BSSID1, SSID2, BSSID2, ...]
        Detects anomalies:
          - Multiple distinct BSSIDs sharing the identical SSID in the same coverage area.
        """
        networks_by_ssid = {}
        for i in range(0, len(raw_network_list), 2):
            if i + 1 < len(raw_network_list):
                ssid = str(raw_network_list[i]).strip()
                bssid = str(raw_network_list[i + 1]).strip()
                if ssid not in networks_by_ssid:
                    networks_by_ssid[ssid] = []
                networks_by_ssid[ssid].append(bssid)

        results = []
        for ssid, bssids in networks_by_ssid.items():
            if len(bssids) > 1:
                # Anomaly detected: Evil Twin candidate!
                for idx, b in enumerate(bssids):
                    status = "LEGITIMATE / FIRST SEEN" if idx == 0 else "🚨 ROGUE AP / EVIL TWIN DETECTED!"
                    results.append({
                        "ssid": ssid,
                        "bssid": b,
                        "is_safe": idx == 0,
                        "threat_level": "CRITICAL" if idx > 0 else "LOW",
                        "status": status
                    })
            else:
                results.append({
                    "ssid": ssid,
                    "bssid": bssids[0],
                    "is_safe": True,
                    "threat_level": "SAFE",
                    "status": "✅ Legitimate Network (Single BSSID)"
                })
        return results

    def run_scan_and_inspect(self):
        print("\n=======================================================")
        print("🛡️  EVIL TWIN NETWORK DEFENDER & THREAT DETECTOR")
        print("=======================================================")
        
        # Display host system audit
        audit = self.get_system_audit()
        print(f"[*] Local Host: {audit['Hostname']} ({audit['OS']})")
        print(f"[*] Connecting to Network Telemetry Gateway at {self.target_host}:{self.target_port}...\n")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5.0)

        try:
            client_socket.connect((self.target_host, self.target_port))
            data = client_socket.recv(4096)
            if not data:
                print("[-] No network beacon data received.")
                return

            raw_networks = ast.literal_eval(data.decode('utf-8'))
            analyzed = self.analyze_networks(raw_networks)

            print(f"[+] Discovered {len(analyzed)} Access Points. Analysis Results:\n")
            print(f"{'#':<3} {'SSID':<22} {'BSSID (MAC)':<20} {'THREAT':<10} {'STATUS'}")
            print("-" * 75)

            for idx, net in enumerate(analyzed, 1):
                print(f"{idx:<3} {net['ssid']:<22} {net['bssid']:<20} {net['threat_level']:<10} {net['status']}")

            # Check if any evil twin rogue AP was detected
            threats = [n for n in analyzed if not n['is_safe']]
            print("\n-------------------------------------------------------")
            if threats:
                print(f"🚨 SECURITY ALERT: {len(threats)} Evil Twin Rogue Access Point(s) Detected!")
                for t in threats:
                    print(f"   ⚠️  Target SSID: '{t['ssid']}' | Spoofed BSSID: {t['bssid']}")
                print("   -> Recommendation: Do NOT connect to this BSSID. Verify router certificate / MAC.")
            else:
                print("✅ All scanned wireless access points appear consistent with single BSSID mapping.")
            print("-------------------------------------------------------")

            # Send defense telemetry report to server
            report_msg = f"Client Inspection Complete: {len(threats)} threats detected out of {len(analyzed)} APs."
            client_socket.sendall(report_msg.encode('utf-8'))

        except ConnectionRefusedError:
            print(f"[-] Could not connect to {self.target_host}:{self.target_port}.")
            print("    Make sure the Attacker Server Simulation is running first!")
        except Exception as e:
            print(f"[-] Detection scan error: {e}")
        finally:
            client_socket.close()
            print("\n[*] Inspection session finished.")

if __name__ == '__main__':
    detector = EvilTwinDetector()
    detector.run_scan_and_inspect()
