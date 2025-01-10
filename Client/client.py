import  socket
from Client.handle_server import handle_server

def start_client():
    try:
        server_host = input("[Client]: Enter the server IP address: ")
        server_port = 12345
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_host, server_port))
        print(f"[Server]: Connected to server at {server_host}:{server_port}")

        # Authenticate with the server
        client_passcode = input("[Client]: Enter the passcode to connect to  the server: ").strup()
        client_socket.send(client_passcode.encode('utf-8'))
        print("[Client]: Authentication request sent to the server. Waiting for response...")

        # Receive authentication response from the server
        response = client_socket.recv(1024).decode('utf-8')
        print(f"[Client]: server response: {response}")
        if response != "Authentication successful.":
            print("[Client]: Authentication failed. Exiting...")
            return
        
        # Pass control to hanndle_server for bidirectional communication
        handle_server(client_socket)
    
    except Exception as e:
        print(f"[Client]: An error ocurred: {e}")
    finally:
        client_socket.close()
        print("[Client]: Disconnected from the server.")