import socket
import ast
import csv
import subprocess


def get_networks():
    attacker_ip = socket.gethostbyname(socket.gethostname())
    attacker_port = 22222  # Update with the attacker's port

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((attacker_ip, attacker_port))
        while True:
            data = client_socket.recv(1024)
            networks = ast.literal_eval(data.decode())

            print("List of Networks:")
            for i in range(0, len(networks), 3):
                ssid = networks[i]
                bssid = networks[i + 1]
                frequency = networks[i + 2]
                print(f"{i // 3 + 1}. SSID: {ssid}, BSSID: {bssid}, Frequency: {frequency}")

            choice = input("Choose a network to check (enter the network number): ")
            try:
                choice = int(choice)
                if 1 <= choice <= len(networks) // 3:
                    selected_ssid = networks[(choice - 1) * 3]
                    is_safe = is_original(selected_ssid, networks)
                    network_type = "Safe" if is_safe else "Evil Twin"
                    print(f"The selected network '{selected_ssid}' is a {network_type} network.")

                    option = input("Choose an action to perform:\n1. Perform speed test\n2. Remove network from list\n3. Continue\n")
                    if option == "1":
                        perform_speed_test(selected_ssid)
                    elif option == "2":
                        remove_network(selected_ssid, networks)
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred: {e}")


def is_original(selected_ssid, networks):
    # Check if the selected SSID exists in the original networks
    original_ssids = networks[::3]
    return selected_ssid in original_ssids


def perform_speed_test(selected_ssid):
    print(f"Performing speed test for network '{selected_ssid}'...")
    command = f"speedtest-cli --simple --server-id=0"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout
    lines = output.split("\n")
    download_speed = lines[0].split()[1]
    upload_speed = lines[1].split()[1]
    print(f"Download Speed: {download_speed} Mbps")
    print(f"Upload Speed: {upload_speed} Mbps")


def remove_network(selected_ssid, networks):
    try:
        with open("networks.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for i in range(0, len(networks), 3):
                ssid = networks[i]
                if ssid != selected_ssid:
                    bssid = networks[i + 1]
                    frequency = networks[i + 2]
                    writer.writerow([ssid, bssid, frequency])
        print(f"Network '{selected_ssid}' has been removed from the list.")
    except Exception as e:
        print(f"An error occurred while removing the network: {e}")


if __name__ == "__main__":
    get_networks()

    input("Press Enter to exit...")