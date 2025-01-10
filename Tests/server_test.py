import unittest
import socket
from threading import Thread
import time
import sys
import os

# Add root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Server.server import start_server
from CryptoOperations.encryption import encrypt_message
from CryptoOperations.decryption import decrypt_message

class TestServer(unittest.TestCase):
    def setUp(self):
        self.server_host = "127.0.0.1"
        self.server_port = 12345
        self.valid_client_passcode = "mypasscode"
        self.valid_message_passcode = "mymessagepasscode"
        self.test_message = "Hello from the server!"

        # Start the server in a separate thread
        self.server_thread = Thread(target=start_server, daemon=True)
        self.server_thread.start()
        time.sleep(2)  # Wait for the server to initialize

    def test_server_handling(self):
        try:
            # Step 1: Connect to the server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.server_host, self.server_port))

            # Step 2: Authenticate with the server
            client_socket.send(self.valid_client_passcode.encode('utf-8'))
            server_response = client_socket.recv(1024).decode('utf-8')
            self.assertEqual(server_response, "Authentication successful.")

            # Step 3: Send an encrypted message
            encrypted_message = encrypt_message(self.test_message, self.valid_message_passcode)
            client_socket.send(encrypted_message)

            # Step 4: Verify server response
            encrypted_response = client_socket.recv(1024)
            iv = encrypted_response[:16]
            encrypted_data = encrypted_response[16:]
            decrypted_response = decrypt_message(encrypted_data, self.valid_message_passcode, iv)

            self.assertIn("Server says:", decrypted_response)

            client_socket.close()
        except Exception as e:
            self.fail(f"Test failed with exception: {e}")

    def tearDown(self):
        # Add any cleanup if needed (e.g., stopping the server)
        pass

if __name__ == "__main__":
    unittest.main()
