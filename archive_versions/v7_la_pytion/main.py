import socket
import threading
import random
import time

networks = []
connected_clients = []

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

def send_networks(client_socket):
    while True:
        create_networks()
        client_socket.send(str(networks).encode())
        time.sleep(10)  # Simulate updates every 10 seconds

def handle_client(client_socket):
    connected_clients.append(client_socket)
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            # Process received data here
    except:
        pass
    finally:
        client_socket.close()
        connected_clients.remove(client_socket)

def server_shutdown(server_socket):
    while True:
        command = input()
        if command == "shutdown":
            for client_socket in connected_clients:
                client_socket.close()
            server_socket.close()
            break

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 22222))  # Replace with the desired port
    server_socket.listen(1)

    shutdown_thread = threading.Thread(target=server_shutdown, args=(server_socket,))
    shutdown_thread.start()

    while True:
        client_socket, _ = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

    shutdown_thread.join()

if __name__ == "__main__":
    main()