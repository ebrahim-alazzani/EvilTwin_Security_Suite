import socket
import ast


def get_networks():
    attacker_ip = socket.gethostbyname(socket.gethostname())   # Update with the attacker's IP or hostname
    attacker_port = 22222  # Update with the attacker's port

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((attacker_ip, attacker_port))
        while True:
            data = b""
            while len(data) < 1024:  # Receive until expected data length is reached
                packet = client_socket.recv(1024)
                if not packet:
                    break
                data += packet

            if not data:
                break

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
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()


def is_original(selected_ssid, networks):
    # Check if the selected SSID exists in the original networks
    original_ssids = networks[::2]
    return selected_ssid in original_ssids


if __name__ == "__main__":
    get_networks()