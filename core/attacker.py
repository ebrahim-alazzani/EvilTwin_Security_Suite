"""
EvilTwin Security Suite - Attacker Simulation Server Module
Simulates Rogue Access Point (Evil Twin) telemetry, broadcasts beacon networks,
and captures victim connection telemetry for educational demonstration and defense verification.
"""

import os
import sys
import socket
import threading
import random
import time
import signal
import platform

try:
    import psutil
except ImportError:
    psutil = None

def get_banner():
    banner = r"""
  ______      _ _   _______          _          _   _             _    
 |  ____|    (_) | |__   __|        (_)        | | | |           | |   
 | |__  __   _| |    | |_      ___  _ _ __     | |_| |_ __ _  ___| | __
 |  __| \ \ / / | |    | \ \ /\ / / | | '_ \    | __| __/ _` |/ __| |/ /
 | |____ \ V /| | |    | |\ V  V /| | | | | |   | |_| || (_| | (__|   < 
 |______| \_/ |_|_|    |_| \_/\_/ |_|_|_| |_|    \__|\__\__,_|\___|_|\_\
                                              [Educational Security Suite]
"""
    return banner

def generate_random_mac():
    mac = [random.randint(0x00, 0xff) for _ in range(6)]
    # Set locally administered bit and unicast
    mac[0] = (mac[0] & 0xfc) | 0x02
    return ':'.join(['{:02x}'.format(x) for x in mac])

class EvilTwinServer:
    def __init__(self, host='0.0.0.0', port=22222, log_dir='logs'):
        self.host = host
        self.port = port
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.server_socket = None
        self.is_running = False
        self.simulated_networks = []
        self._init_simulated_networks()

    def _init_simulated_networks(self):
        original_bssid = generate_random_mac()
        twin_bssid = generate_random_mac()
        
        # Original network vs Rogue / Twin network
        self.simulated_networks = [
            {"ssid": "Corporate_WiFi", "bssid": original_bssid, "is_safe": True, "type": "Original AP"},
            {"ssid": "Corporate_WiFi", "bssid": twin_bssid, "is_safe": False, "type": "Evil Twin Rogue AP"},
            {"ssid": "Campus_Guest", "bssid": generate_random_mac(), "is_safe": True, "type": "Original AP"}
        ]

    def get_system_telemetry(self):
        info = []
        info.append(f"OS: {platform.system()} {platform.release()} ({platform.architecture()[0]})")
        info.append(f"Hostname: {platform.node()}")
        info.append(f"Processor: {platform.processor() or 'Standard x86/x64'}")
        info.append(f"Python: {platform.python_version()}")

        if psutil:
            try:
                mem = psutil.virtual_memory()
                info.append(f"Memory: {round(mem.total / (1024**3), 2)} GB (Used: {mem.percent}%)")
                users = psutil.users()
                user_list = [u.name for u in users] if users else ['None']
                info.append(f"Active Users: {', '.join(user_list)}")
            except Exception:
                pass
        return "\n".join(info)

    def log_session(self, client_ip, client_port, data):
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        log_file = os.path.join(self.log_dir, f"session_{client_ip}_{client_port}_{timestamp}.log")
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"=== EVIL TWIN CAPTURE SESSION ===\n")
                f.write(f"Timestamp: {time.ctime()}\n")
                f.write(f"Client IP: {client_ip}:{client_port}\n")
                f.write(f"Data:\n{data}\n")
            print(f"[+] Session telemetry logged to: {log_file}")
        except Exception as e:
            print(f"[-] Failed to log session: {e}")

    def handle_client(self, client_sock, client_addr):
        client_ip, client_port = client_addr
        print(f"[!] New client connection from {client_ip}:{client_port}")

        try:
            # Flatten networks into serializable payload
            net_payload = []
            for n in self.simulated_networks:
                net_payload.extend([n["ssid"], n["bssid"]])

            # Send networks list to client
            client_sock.sendall(str(net_payload).encode('utf-8'))

            # Receive client response / notification
            data = client_sock.recv(4096).decode('utf-8', errors='ignore')
            if data:
                print(f"[+] Received response from {client_ip}: {data[:120]}")
                telemetry = self.get_system_telemetry()
                self.log_session(client_ip, client_port, f"Client Report: {data}\n\nServer Telemetry:\n{telemetry}")

        except Exception as e:
            print(f"[-] Client connection error ({client_ip}): {e}")
        finally:
            try:
                client_sock.close()
            except Exception:
                pass
            print(f"[*] Connection with {client_ip}:{client_port} closed.")

    def start(self):
        self.is_running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(get_banner())
            print(f"[+] Evil Twin Server started on {self.host}:{self.port}")
            print(f"[+] Broadcast simulated beacon networks:")
            for n in self.simulated_networks:
                print(f"    - SSID: {n['ssid']} | BSSID: {n['bssid']} [{n['type']}]")
            print("\n[*] Waiting for connections... (Press Ctrl+C to stop)\n")

            while self.is_running:
                try:
                    self.server_socket.settimeout(1.0)
                    client_sock, client_addr = self.server_socket.accept()
                    t = threading.Thread(target=self.handle_client, args=(client_sock, client_addr), daemon=True)
                    t.start()
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.is_running:
                        print(f"[-] Accept error: {e}")

        except Exception as e:
            print(f"[-] Server error: {e}")
        finally:
            self.stop()

    def stop(self):
        self.is_running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass
        print("\n[+] Evil Twin Server stopped gracefully.")

def run_standalone():
    server = EvilTwinServer()
    def sig_handler(sig, frame):
        server.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    server.start()

if __name__ == '__main__':
    run_standalone()
