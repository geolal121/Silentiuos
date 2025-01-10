import socket
import threading
from Client.handle_server import handle_server
from CleanUp.CleanUp import CleanUp
from CleanUp.NoActivity import NoActivityMonitor

def start_client():
    try:
        server_host = input("[Client]: Enter the server IP address: ")
        server_port = 12345
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_host, server_port))
        print(f"[Server]: Connected to server at {server_host}:{server_port}")

        # Authenticate with the server
        client_passcode = input("[Client]: Enter the passcode to connect to the server: ").strip()
        client_socket.send(client_passcode.encode('utf-8'))
        print("[Client]: Authentication request sent to the server. Waiting for response...")

        # Receive authentication response from the server
        response = client_socket.recv(1024).decode('utf-8')
        print(f"[Client]: Server response: {response}")
        if response != "Authentication successful.":
            print("[Client]: Authentication failed. Exiting...")
            return

        # Start NoActivityMonitor
        inactivity_monitor = NoActivityMonitor(timeout=300, server_socket=client_socket)
        monitor_thread = threading.Thread(target=inactivity_monitor.start_monitoring, daemon=True)
        monitor_thread.start()

        # Pass control to handle_server for bidirectional communication
        handle_server(client_socket, inactivity_monitor)

    except Exception as e:
        print(f"[Client]: An error occurred: {e}")
    finally:
        client_socket.close()
        CleanUp.clear_terminal()
        print("[Client]: Disconnected from the server.")