import os
import socket
import threading
import random
import time
import signal
import sys
import psutil
import platform
import keyboard

networks = []

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def go_back():
    clear_screen()
    main_menu()

def exit_program():
    clear_screen()
    print("Exiting...")
    sys.exit(0)

def main_menu():
    print("Main Menu:")
    print("1. Start listening for connections")
    print("2. Exit")

    choice = input("Enter your choice: ")
    if choice == "1":
        start_server()
    elif choice == "2":
        exit_program()
    else:
        print("Invalid choice. Please try again.")
        main_menu()

def generate_mac_address():
    mac = [random.randint(0x00, 0xff) for _ in range(6)]
    return ':'.join(['{:02x}'.format(x) for x in mac])

def start_server():
    signal.signal(signal.SIGINT, server_shutdown)

    clear_screen()
    print("Server started. Listening for connections...")
    print("----------------------------------------------")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 22222))  # Replace with the desired port
    server_socket.listen(1)

    accept_thread = threading.Thread(target=accept_connections, args=(server_socket,))
    accept_thread.start()

    keyboard.add_hotkey('esc', go_back)
    keyboard.wait('ctrl+esc')

def accept_connections(server_socket):
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

        network_thread = threading.Thread(target=send_networks, args=(client_socket,))
        network_thread.start()

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
    get_network_info()

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

    users = psutil.users()
    if users:
        print("Users:")
        for user in users:
            print(f"Username: {user.name}")
    else:
        print("No users found.")

def get_network_info():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    connected_network = "N/A"
    router_name = "N/A"

    wifi_networks = [network for network in networks if network.startswith("SSID:")]
    if wifi_networks:
        connected_network = wifi_networks[0].replace("SSID:", "").strip()
        router_name = wifi_networks[1].replace("SSID:", "").strip() if len(wifi_networks) > 1 else "N/A"

    subscribers = len(wifi_networks) - 2 if len(wifi_networks) > 2 else 0

    print("Network Information:")
    print(f"Connected Network (SSID): {connected_network}")
    print(f"Router Name (SSID): {router_name}")
    print(f"Main IP Address: {local_ip}")
    print(f"Number of Wi-Fi Subscribers: {subscribers}")

def send_networks(client_socket):
    get_system_info()
    while True:
        create_networks()
        try:
            client_socket.sendall(str(networks).encode())
        except socket.error as e:
            print(f"Error sending data: {str(e)}")
            break
        except Exception as ex:
            print(f"Exception occurred: {str(ex)}")
            break
        time.sleep(20)  # Simulate updates every 20 seconds

def server_shutdown(signum, frame):
    clear_screen()
    print("Server shutting down...")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, server_shutdown)

    clear_screen()
   
    main_menu()

if __name__ == "__main__":
    main()