"""
=============================================================================
 EvilTwin Security Suite - Cyber Modern GUI Edition (English Interface)
 High-Tech Dark Cyberpunk Theme with CustomTkinter.
 Real-Time Telemetry, Rogue AP Broadcasts & Wireless Threat Detector.
=============================================================================
"""

import sys
import os
import time
import socket
import threading
import platform
import tkinter as tk
from tkinter import messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import customtkinter as ctk

try:
    import psutil
except ImportError:
    psutil = None

from core.attacker import EvilTwinServer
from core.detector import EvilTwinDetector

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class EvilTwinGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("EvilTwin Security Suite | Cyber Defense Center")
        self.geometry("1120x760")
        self.minsize(980, 680)

        self.server_instance = None
        self.server_thread = None
        self.is_server_running = False

        self._setup_grid()
        self._build_sidebar()
        self._build_main_container()

        self.show_dashboard_view()

    def _setup_grid(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def _build_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color="#0d1117")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="🛡️ EVIL TWIN\nSECURITY SUITE", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#00ffff"
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(25, 20))

        self.btn_dashboard = ctk.CTkButton(
            self.sidebar_frame, text="📊 Dashboard & Telemetry", 
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1f2937", hover_color="#374151", height=42, anchor="w",
            command=self.show_dashboard_view
        )
        self.btn_dashboard.grid(row=1, column=0, padx=15, pady=8, sticky="ew")

        self.btn_attacker = ctk.CTkButton(
            self.sidebar_frame, text="⚡ Rogue AP Simulator", 
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1f2937", hover_color="#b91c1c", height=42, anchor="w",
            command=self.show_attacker_view
        )
        self.btn_attacker.grid(row=2, column=0, padx=15, pady=8, sticky="ew")

        self.btn_detector = ctk.CTkButton(
            self.sidebar_frame, text="🔍 Threat Detector", 
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1f2937", hover_color="#047857", height=42, anchor="w",
            command=self.show_detector_view
        )
        self.btn_detector.grid(row=3, column=0, padx=15, pady=8, sticky="ew")

        self.btn_audit = ctk.CTkButton(
            self.sidebar_frame, text="🌐 Network Audit", 
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1f2937", hover_color="#374151", height=42, anchor="w",
            command=self.show_audit_view
        )
        self.btn_audit.grid(row=4, column=0, padx=15, pady=8, sticky="ew")

        self.btn_logs = ctk.CTkButton(
            self.sidebar_frame, text="📁 Captured Logs", 
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1f2937", hover_color="#374151", height=42, anchor="w",
            command=self.show_logs_view
        )
        self.btn_logs.grid(row=5, column=0, padx=15, pady=8, sticky="ew")

        self.btn_docs = ctk.CTkButton(
            self.sidebar_frame, text="📖 Documentation", 
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1f2937", hover_color="#374151", height=42, anchor="w",
            command=self.show_docs_view
        )
        self.btn_docs.grid(row=6, column=0, padx=15, pady=8, sticky="ew")

        self.lbl_system = ctk.CTkLabel(
            self.sidebar_frame,
            text=f"Platform: {platform.system()} {platform.release()}\nPython: {platform.python_version()}",
            font=ctk.CTkFont(size=11),
            text_color="#9ca3af"
        )
        self.lbl_system.grid(row=8, column=0, padx=15, pady=15, sticky="s")

    def _build_main_container(self):
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="#161b22")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

    def _clear_main_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def _highlight_button(self, active_button):
        for btn in [self.btn_dashboard, self.btn_attacker, self.btn_detector, self.btn_audit, self.btn_logs, self.btn_docs]:
            if btn == active_button:
                btn.configure(fg_color="#2563eb")
            else:
                btn.configure(fg_color="#1f2937")

    # =========================================================================
    # VIEW 1: Dashboard
    # =========================================================================
    def show_dashboard_view(self):
        self._clear_main_container()
        self._highlight_button(self.btn_dashboard)

        scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        scroll.grid(row=0, column=0, sticky="nsew", padx=25, pady=20)
        scroll.grid_columnconfigure((0, 1, 2), weight=1)

        title_box = ctk.CTkFrame(scroll, fg_color="#1f2937", corner_radius=12)
        title_box.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 20), padx=5)

        title = ctk.CTkLabel(
            title_box, 
            text="⚡ Wireless Threat Intelligence & Evil Twin Simulation Dashboard",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#60a5fa"
        )
        title.pack(padx=20, pady=15, anchor="w")

        card1 = self._create_metric_card(scroll, "Rogue AP Status", "STOPPED" if not self.is_server_running else "ACTIVE / BROADCASTING", "#ef4444" if not self.is_server_running else "#10b981")
        card2 = self._create_metric_card(scroll, "Simulation Port", "Port: 22222", "#3b82f6")
        card3 = self._create_metric_card(scroll, "Defense & Integrity", "HIGH (Ready)", "#10b981")

        card1.grid(row=1, column=0, padx=8, pady=10, sticky="nsew")
        card2.grid(row=1, column=1, padx=8, pady=10, sticky="nsew")
        card3.grid(row=1, column=2, padx=8, pady=10, sticky="nsew")

        info_frame = ctk.CTkFrame(scroll, fg_color="#0f172a", corner_radius=12, border_width=1, border_color="#334155")
        info_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=15, padx=5)

        info_lbl = ctk.CTkLabel(
            info_frame,
            text=(
                "🛡️ EvilTwin Security Suite - Professional Wireless Research Framework\n\n"
                "• Simulates Rogue Access Points (Evil Twin APs) beaconing identical network SSIDs.\n"
                "• Autonomous Threat Detector scans and detects BSSID/MAC anomalies in real-time.\n"
                "• Historical versions and source evolution archived under 'archive_versions/' folder."
            ),
            font=ctk.CTkFont(size=14),
            justify="left",
            text_color="#e2e8f0"
        )
        info_lbl.pack(padx=25, pady=20, fill="both")

        btn_box = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_box.grid(row=3, column=0, columnspan=3, pady=10)

        ctk.CTkButton(
            btn_box, text="🚀 Launch Attacker Server", 
            fg_color="#dc2626", hover_color="#b91c1c", width=220, height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.show_attacker_view
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_box, text="🛡️ Run Threat Detector", 
            fg_color="#059669", hover_color="#047857", width=220, height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.show_detector_view
        ).pack(side="left", padx=10)

    def _create_metric_card(self, parent, title, value, color):
        card = ctk.CTkFrame(parent, fg_color="#111827", corner_radius=12, border_width=1, border_color="#1f2937")
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=13), text_color="#9ca3af").pack(padx=15, pady=(15, 5), anchor="w")
        ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=17, weight="bold"), text_color=color).pack(padx=15, pady=(0, 15), anchor="w")
        return card

    # =========================================================================
    # VIEW 2: Attacker Simulation Server
    # =========================================================================
    def show_attacker_view(self):
        self._clear_main_container()
        self._highlight_button(self.btn_attacker)

        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=25, pady=20)

        ctk.CTkLabel(
            frame, text="⚡ Rogue Access Point Simulator (Attacker Server)",
            font=ctk.CTkFont(size=20, weight="bold"), text_color="#f87171"
        ).pack(anchor="w", pady=(0, 10))

        ctrl_box = ctk.CTkFrame(frame, fg_color="#1f2937", corner_radius=12)
        ctrl_box.pack(fill="x", pady=10)

        ctk.CTkLabel(ctrl_box, text="Server Port:", font=ctk.CTkFont(size=13)).pack(side="left", padx=(15, 5), pady=15)
        self.entry_port = ctk.CTkEntry(ctrl_box, width=90, justify="center")
        self.entry_port.insert(0, "22222")
        self.entry_port.pack(side="left", padx=5, pady=15)

        self.btn_toggle_server = ctk.CTkButton(
            ctrl_box, 
            text="Start Server 🚀" if not self.is_server_running else "Stop Server 🛑",
            fg_color="#dc2626" if not self.is_server_running else "#4b5563",
            hover_color="#b91c1c" if not self.is_server_running else "#374151",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.toggle_server
        )
        self.btn_toggle_server.pack(side="left", padx=20, pady=15)

        self.lbl_server_status = ctk.CTkLabel(
            ctrl_box, 
            text="● Server Inactive" if not self.is_server_running else "● Server Active & Listening...",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#9ca3af" if not self.is_server_running else "#10b981"
        )
        self.lbl_server_status.pack(side="left", padx=10, pady=15)

        ctk.CTkLabel(frame, text="Live Broadcast & Session Stream:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(15, 5))
        self.txt_server_log = ctk.CTkTextbox(frame, fg_color="#030712", text_color="#22c55e", font=ctk.CTkFont(family="Consolas", size=13))
        self.txt_server_log.pack(fill="both", expand=True)

        if self.is_server_running:
            self.txt_server_log.insert("end", "[+] Server is currently broadcasting simulated beacons...\n")

    def toggle_server(self):
        if not self.is_server_running:
            port_val = self.entry_port.get().strip()
            port = int(port_val) if port_val.isdigit() else 22222
            self.server_instance = EvilTwinServer(port=port)
            self.is_server_running = True
            self.btn_toggle_server.configure(text="Stop Server 🛑", fg_color="#4b5563", hover_color="#374151")
            self.lbl_server_status.configure(text="● Server Active & Listening...", text_color="#10b981")
            
            self.txt_server_log.insert("end", f"[*] Attacker Simulation Server started on port: {port}\n")
            self.txt_server_log.insert("end", "[*] Broadcasting Rogue Evil Twin Beacons...\n")

            def run_server():
                try:
                    self.server_instance.start()
                except Exception as e:
                    self.txt_server_log.insert("end", f"[!] Server Exception: {e}\n")

            self.server_thread = threading.Thread(target=run_server, daemon=True)
            self.server_thread.start()
        else:
            if self.server_instance:
                self.server_instance.stop()
            self.is_server_running = False
            self.btn_toggle_server.configure(text="Start Server 🚀", fg_color="#dc2626", hover_color="#b91c1c")
            self.lbl_server_status.configure(text="● Server Inactive", text_color="#9ca3af")
            self.txt_server_log.insert("end", "[!] Server stopped successfully.\n")

    # =========================================================================
    # VIEW 3: Threat Detector
    # =========================================================================
    def show_detector_view(self):
        self._clear_main_container()
        self._highlight_button(self.btn_detector)

        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=25, pady=20)

        ctk.CTkLabel(
            frame, text="🔍 Evil Twin Threat Detector & Network Defender",
            font=ctk.CTkFont(size=20, weight="bold"), text_color="#34d399"
        ).pack(anchor="w", pady=(0, 10))

        cfg_box = ctk.CTkFrame(frame, fg_color="#1f2937", corner_radius=12)
        cfg_box.pack(fill="x", pady=10)

        ctk.CTkLabel(cfg_box, text="Target Host:", font=ctk.CTkFont(size=13)).pack(side="left", padx=(15, 5), pady=15)
        self.entry_det_host = ctk.CTkEntry(cfg_box, width=120, justify="center")
        self.entry_det_host.insert(0, "127.0.0.1")
        self.entry_det_host.pack(side="left", padx=5, pady=15)

        ctk.CTkLabel(cfg_box, text="Port:", font=ctk.CTkFont(size=13)).pack(side="left", padx=(15, 5), pady=15)
        self.entry_det_port = ctk.CTkEntry(cfg_box, width=80, justify="center")
        self.entry_det_port.insert(0, "22222")
        self.entry_det_port.pack(side="left", padx=5, pady=15)

        self.btn_scan = ctk.CTkButton(
            cfg_box, text="Run Security Scan 🛡️",
            fg_color="#059669", hover_color="#047857",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.run_detector_scan
        )
        self.btn_scan.pack(side="left", padx=20, pady=15)

        ctk.CTkLabel(frame, text="Network Anomaly Analysis & Rogue AP Detections:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(15, 5))
        self.txt_det_log = ctk.CTkTextbox(frame, fg_color="#030712", text_color="#38bdf8", font=ctk.CTkFont(family="Consolas", size=13))
        self.txt_det_log.pack(fill="both", expand=True)

    def run_detector_scan(self):
        host = self.entry_det_host.get().strip() or "127.0.0.1"
        port_val = self.entry_det_port.get().strip()
        port = int(port_val) if port_val.isdigit() else 22222

        self.txt_det_log.delete("1.0", "end")
        self.txt_det_log.insert("end", f"[*] Probing target host: {host}:{port} for beacon frames...\n\n")

        def task():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5.0)
                s.connect((host, port))
                banner = s.recv(4096).decode('utf-8', errors='ignore')
                raw_data = s.recv(4096).decode('utf-8', errors='ignore').strip()
                s.close()

                import ast
                net_list = ast.literal_eval(raw_data)
                detector = EvilTwinDetector(target_host=host, target_port=port)
                results = detector.analyze_networks(net_list)

                self.txt_det_log.insert("end", "[+] Wireless Beacon Frames Received Successfully!\n")
                self.txt_det_log.insert("end", "=" * 70 + "\n")
                
                alert_count = 0
                for item in results:
                    ssid = item['ssid']
                    bssid = item['bssid']
                    status = item['status']
                    threat = item['threat_level']

                    if threat == "CRITICAL":
                        alert_count += 1
                        self.txt_det_log.insert("end", f"\n🚨 [CRITICAL SECURITY ALERT!]\n")
                        self.txt_det_log.insert("end", f"  * Impersonated Network (SSID) : {ssid}\n")
                        self.txt_det_log.insert("end", f"  * Detected Rogue MAC (BSSID)  : {bssid}\n")
                        self.txt_det_log.insert("end", f"  * Assessment                  : Multiple disparate BSSIDs detected for identical SSID!\n")
                        self.txt_det_log.insert("end", f"  * Remediation                 : Disconnect immediately. Enforce WPA3/Enterprise.\n")
                    else:
                        self.txt_det_log.insert("end", f"\n✅ [VERIFIED / LEGITIMATE NETWORK]\n")
                        self.txt_det_log.insert("end", f"  * Network SSID  : {ssid}\n")
                        self.txt_det_log.insert("end", f"  * Router BSSID  : {bssid}\n")
                    self.txt_det_log.insert("end", "-" * 70 + "\n")

                if alert_count > 0:
                    messagebox.showwarning(
                        "Evil Twin Attack Detected!",
                        f"CRITICAL WARNING:\nDetected {alert_count} Rogue Access Point(s) impersonating legitimate network SSIDs!"
                    )
            except Exception as e:
                self.txt_det_log.insert("end", f"[!] Connection failed ({host}:{port}): {e}\n")
                self.txt_det_log.insert("end", "[-] Make sure the 'Rogue AP Simulator' is running first.\n")

        threading.Thread(target=task, daemon=True).start()

    # =========================================================================
    # VIEW 4: Network Audit
    # =========================================================================
    def show_audit_view(self):
        self._clear_main_container()
        self._highlight_button(self.btn_audit)

        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=25, pady=20)

        ctk.CTkLabel(
            frame, text="🌐 Network Interface & System Telemetry Audit",
            font=ctk.CTkFont(size=20, weight="bold"), text_color="#60a5fa"
        ).pack(anchor="w", pady=(0, 10))

        txt_audit = ctk.CTkTextbox(frame, fg_color="#030712", text_color="#cbd5e1", font=ctk.CTkFont(family="Consolas", size=13))
        txt_audit.pack(fill="both", expand=True)

        hostname = socket.gethostname()
        try:
            local_ip = socket.gethostbyname(hostname)
        except Exception:
            local_ip = "127.0.0.1"

        txt_audit.insert("end", f"[*] Hostname          : {hostname}\n")
        txt_audit.insert("end", f"[*] Primary Local IP  : {local_ip}\n")
        txt_audit.insert("end", f"[*] OS Architecture   : {platform.system()} {platform.release()} ({platform.machine()})\n")
        txt_audit.insert("end", "=" * 75 + "\n\n")

        if psutil:
            addrs = psutil.net_if_addrs()
            stats = psutil.net_if_stats()
            for iface, addr_list in addrs.items():
                stat = stats.get(iface)
                status_str = "CONNECTED [UP]" if (stat and stat.isup) else "DISCONNECTED [DOWN]"
                speed = f"{stat.speed}Mbps" if (stat and stat.speed > 0) else "N/A"
                txt_audit.insert("end", f"* Adapter: {iface} [{status_str} | Speed: {speed}]\n")
                for a in addr_list:
                    family = "IPv4" if a.family == socket.AF_INET else ("MAC" if hasattr(psutil, 'AF_LINK') and a.family == psutil.AF_LINK else str(a.family))
                    txt_audit.insert("end", f"    - {family}: {a.address}\n")
                txt_audit.insert("end", "\n")
        else:
            txt_audit.insert("end", "[!] 'psutil' is not available for full adapter enumeration.\n")

    # =========================================================================
    # VIEW 5: Captured Logs
    # =========================================================================
    def show_logs_view(self):
        self._clear_main_container()
        self._highlight_button(self.btn_logs)

        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=25, pady=20)

        ctk.CTkLabel(
            frame, text="📁 Captured Session Logs (Logs Viewer)",
            font=ctk.CTkFont(size=20, weight="bold"), text_color="#fbbf24"
        ).pack(anchor="w", pady=(0, 10))

        log_dir = os.path.join(BASE_DIR, 'logs')
        os.makedirs(log_dir, exist_ok=True)

        txt_logs = ctk.CTkTextbox(frame, fg_color="#030712", text_color="#fde047", font=ctk.CTkFont(family="Consolas", size=13))
        txt_logs.pack(fill="both", expand=True)

        log_files = [f for f in os.listdir(log_dir) if f.endswith('.log') or f.endswith('.txt')]
        if not log_files:
            txt_logs.insert("end", "[-] No session log files found.\nAny connection capture will be recorded automatically here.")
        else:
            txt_logs.insert("end", f"[+] Found {len(log_files)} log file(s):\n\n")
            for lf in log_files:
                fp = os.path.join(log_dir, lf)
                txt_logs.insert("end", f"=== File: {lf} ({os.path.getsize(fp)} bytes) ===\n")
                try:
                    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                        txt_logs.insert("end", f.read())
                except Exception as e:
                    txt_logs.insert("end", f"[Error reading file: {e}]\n")
                txt_logs.insert("end", "\n" + "=" * 65 + "\n\n")

    # =========================================================================
    # VIEW 6: Documentation
    # =========================================================================
    def show_docs_view(self):
        self._clear_main_container()
        self._highlight_button(self.btn_docs)

        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=25, pady=20)

        ctk.CTkLabel(
            frame, text="📖 Documentation & Theoretical Concepts",
            font=ctk.CTkFont(size=20, weight="bold"), text_color="#a78bfa"
        ).pack(anchor="w", pady=(0, 10))

        txt_docs = ctk.CTkTextbox(frame, fg_color="#0f172a", text_color="#e2e8f0", font=ctk.CTkFont(size=14))
        txt_docs.pack(fill="both", expand=True)

        docs_content = """
1. What is an Evil Twin Attack?
   • A cyber wireless attack where an adversary deploys a rogue Wi-Fi Access Point (AP).
   • The rogue AP broadcasts the exact same Service Set Identifier (SSID) as a legitimate network.

2. Exploitation Mechanics:
   • Client wireless cards associate with whichever AP provides the strongest signal.
   • Attackers can broadcast 802.11 Deauthentication packets to forcibly kick victims off 
     the genuine router, pushing them into the rogue AP trap.
   • The attacker acts as a Man-in-the-Middle (MitM), snooping and intercepting unencrypted data.

3. Detection Logic:
   • The detector scans local wireless beacons and pairs (SSID, BSSID).
   • If multiple distinct BSSIDs (MAC addresses) are registered for the same SSID within 
     the coverage vicinity, the engine flags an immediate Rogue AP / Evil Twin alert.

4. Recommended Defenses:
   • Utilize WPA3-Personal or 802.1X Enterprise authentication.
   • Enforce end-to-end encrypted VPN tunnels over public hotspots.
   • Deploy Wireless Intrusion Detection Systems (WIDS/WIPS).
"""
        txt_docs.insert("end", docs_content.strip())

if __name__ == "__main__":
    app = EvilTwinGUI()
    app.mainloop()
