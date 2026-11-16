"""
EvilTwin Security Suite - Wireless MITM Utilities (Linux / Advanced Environments)
Adapted from Version 8 historical research scripts (hostapd, dnsmasq, packet forwarding).
"""

import subprocess
import shutil
import os
import platform

def is_linux():
    return platform.system().lower() == 'linux'

def enable_packet_forwarding():
    """Enables IPv4 forwarding on Linux kernels."""
    if not is_linux():
        print("[!] Packet forwarding is only applicable on Linux testbeds.")
        return False
    try:
        with open('/proc/sys/net/ipv4/ip_forward', 'w') as fd:
            fd.write('1')
        print("[+] IPv4 packet forwarding enabled.")
        return True
    except PermissionError:
        print("[-] Root privileges required to enable packet forwarding.")
        return False
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

def disable_packet_forwarding():
    """Disables IPv4 forwarding on Linux kernels."""
    if not is_linux():
        return False
    try:
        with open('/proc/sys/net/ipv4/ip_forward', 'w') as fd:
            fd.write('0')
        print("[+] IPv4 packet forwarding disabled.")
        return True
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

class IPTablesManager:
    """Manages NAT and port-forwarding rules for rogue access points."""
    def __init__(self, upstream_interface='eth0', ap_interface='wlan0'):
        self.upstream = upstream_interface
        self.ap_iface = ap_interface

    def setup_nat(self):
        if not is_linux():
            print("[!] IPTables configuration requires a Linux operating system.")
            return False
        cmds = [
            f"iptables -t nat -A POSTROUTING -o {self.upstream} -j MASQUERADE",
            f"iptables -A FORWARD -i {self.ap_iface} -o {self.upstream} -j ACCEPT",
            f"iptables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT"
        ]
        for cmd in cmds:
            try:
                subprocess.run(cmd.split(), check=True)
            except Exception as e:
                print(f"[-] Failed executing '{cmd}': {e}")
                return False
        print("[+] NAT routing successfully configured.")
        return True

    def flush(self):
        if not is_linux(): return
        subprocess.run(["iptables", "-F"])
        subprocess.run(["iptables", "-t", "nat", "-F"])
        print("[+] IPTables flushed.")
