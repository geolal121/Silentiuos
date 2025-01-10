import socket
import threading
from CleanUp.NoActivity import NoActivityMonitor
from CleanUp.CleanUp import CleanUp
from Authentication.authentication import authenticate_client
from Server.handle_client import handle_client

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 12345
all_clients = []

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"[Server]: Server started on {SERVER_HOST}:{SERVER_PORT}")

    # Start the inactivity monitor
    inactivity_monitor = NoActivityMonitor(timeout=90, all_clients=all_clients, server_socket=server_socket)
    monitor_thread = threading.Thread(target=inactivity_monitor.start_monitoring, daemon=True)
    monitor_thread.start()

    def accept_clients():
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                print(f"[Server]: Connection from {client_address}")
                all_clients.append(client_socket)

                # Reset inactivity timer on new connection
                inactivity_monitor.update_activity()

                # Start a new thread to handle the client
                client_thread = threading.Thread(
                    target=handle_client,
                    args=(client_socket, client_address, all_clients, inactivity_monitor)
                )
                client_thread.start()
            except OSError:
                # Socket closed, exit the loop
                break

    # Start the client acceptance loop in a separate thread
    accept_thread = threading.Thread(target=accept_clients)
    accept_thread.start()

    try:
        # Listen for the server admin's "exit" command
        while True:
            command = input("[Server]: Enter 'exit' to shut down the server: ").strip().lower()
            if command == "exit":
                print("[Server]: Shutting down the server...")
                break
            inactivity_monitor.update_activity()  # Reset timer on admin input
    except KeyboardInterrupt:
        print("[Server]: Forced shutdown initiated...")

    # Cleanup
    CleanUp.clean_resources(all_clients, server_socket)
    CleanUp.clear_terminal()
    print("[Server]: Server has been stopped.")
