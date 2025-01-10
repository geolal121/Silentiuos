import unittest
import socket
import threading
import sys
import os
import time

# Add root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from CryptoOperations.encryption import encrypt_message
from CryptoOperations.decryption import decrypt_message

class TestClient(unittest.TestCase):
    def setUp(self):
        self.server_host = "127.0.0.1"
        self.server_port = 0  # Use dynamic port
        self.valid_client_passcode = "mypasscode"
        self.valid_message_passcode = "mymessagepasscode"
        self.test_message = "Hello from the client!"

        # Start a mock server in a separate thread
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_host, self.server_port))
        self.server_port = self.server_socket.getsockname()[1]  # Get assigned port
        self.server_socket.listen(5)

        self.server_thread = threading.Thread(target=self.mock_server, daemon=True)
        self.server_thread.start()
        time.sleep(1)  # Allow server time to start

    def mock_server(self):
        while True:
            try:
                client_socket, _ = self.server_socket.accept()
                passcode = client_socket.recv(1024).decode('utf-8')
                if passcode == self.valid_client_passcode:
                    client_socket.send("Authentication successful.".encode('utf-8'))
                    
                    # Receive encrypted message
                    encrypted_message = client_socket.recv(1024)
                    iv = encrypted_message[:16]
                    encrypted_data = encrypted_message[16:]
                    decrypted_message = decrypt_message(encrypted_data, self.valid_message_passcode, iv)

                    # Respond with a processed message
                    response_message = f"Server received: {decrypted_message}"
                    encrypted_response = encrypt_message(response_message, self.valid_message_passcode)
                    client_socket.send(encrypted_response)
                else:
                    client_socket.send("Authentication failed.".encode('utf-8'))
                client_socket.close()
            except Exception as e:
                print(f"[Mock Server] Error: {e}")

    def tearDown(self):
        if hasattr(self, 'server_socket'):
            self.server_socket.close()

    def test_client_connection_and_message(self):
        # Connect to the mock server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.server_host, self.server_port))

        # Step 1: Authenticate with the server
        client_socket.send(self.valid_client_passcode.encode('utf-8'))
        server_response = client_socket.recv(1024).decode('utf-8')
        self.assertEqual(server_response, "Authentication successful.")

        # Step 2: Send an encrypted message
        encrypted_message = encrypt_message(self.test_message, self.valid_message_passcode)
        client_socket.send(encrypted_message)

        # Step 3: Receive and decrypt server response
        encrypted_response = client_socket.recv(1024)
        iv = encrypted_response[:16]
        encrypted_data = encrypted_response[16:]
        decrypted_response = decrypt_message(encrypted_data, self.valid_message_passcode, iv)

        self.assertIn("Server received:", decrypted_response)

        client_socket.close()

if __name__ == "__main__":
    unittest.main()
