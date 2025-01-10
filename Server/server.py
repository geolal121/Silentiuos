import socket
import threading
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

    while True:
        # Accept a new client connection
        client_socket, client_address = server_socket.accept()
        print(f"[Server]: Connection from {client_address}")
        all_clients.append(client_socket)
        # Start a new thread to handle the client
        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address, all_clients)
        )
        client_thread.start()
