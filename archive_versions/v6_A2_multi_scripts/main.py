import platform
import socket
import threading
import random
import time
import signal
import sys

networks = []


def generate_mac_address():
    mac = [random.randint(0x00, 0xff) for _ in range(6)]
    return ':'.join(['{:02x}'.format(x) for x in mac])


def create_networks():
    original_ssid = "OriginalNetwork"
    original_bssid = generate_mac_address()
    twin_ssid = original_ssid
    twin_bssid = generate_mac_address()
    networks.clear()

    networks.append(original_ssid)
    networks.append(original_bssid)
    networks.append(twin_ssid)
    networks.append(twin_bssid)

    print(f"Creating Original Network - SSID: {original_ssid}, BSSID: {original_bssid}")
    print(f"Creating Twin Network - SSID: {twin_ssid}, BSSID: {twin_bssid}")

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
def send_networks(client_socket):
    get_system_info()
    while True:
        create_networks()
        try:
            client_socket.sendall(str(networks).encode())

        except socket.error as e:
            print(f"Error sending data: {str(e)}")
            break
        time.sleep(10)  # Simulate updates every 30 seconds


def server_shutdown(signum, frame):
    print("Server shutting down...")
    sys.exit(0)


def accept_connections(server_socket):
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

        network_thread = threading.Thread(target=send_networks, args=(client_socket,))
        network_thread.start()


def main():
    signal.signal(signal.SIGINT, server_shutdown)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 22222))  # Replace with the desired port
    server_socket.listen(1)

    accept_thread = threading.Thread(target=accept_connections, args=(server_socket,))
    accept_thread.start()

    accept_thread.join()
    server_socket.close()


if __name__ == "__main__":
    main()

input("Press Enter to exit...")