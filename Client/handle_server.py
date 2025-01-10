from Authentication.authentication import authenticate_message
from CryptoOperations.encryption import encrypt_message
from CryptoOperations.decryption import decrypt_message
import base64

def handle_server(server_socket, inactivity_monitor):
    try:
        while True:
            # Reset the inactivity timer
            inactivity_monitor.update_activity()

            # Send a message to the server
            message = input("[Client]: Enter your message (or type 'exit' to quit): ")
            if message.lower() == 'exit':
                print("[Client]: Exiting chat...")
                server_socket.send(b"exit")  # Notify the server about the exit
                break

            # Encrypt the message and send it
            encrypted_message = encrypt_message(message, "mymessagepasscode")
            server_socket.send(encrypted_message)
            print("[Client]: Encrypted message sent to server.")

            # Wait for the server's response
            print("[Client]: Waiting for server response...")
            encrypted_response = server_socket.recv(4096)
            if not encrypted_response:
                print("[Client]: Server has disconnected.")
                break

            # Show the encrypted message in hexadecimal format
            print("[Client]: Encrypted message received from server:")
            print(base64.b64encode(encrypted_response).decode('utf-8'))

            # Prompt the user to enter the passcode to decrypt
            server_message_passcode = input("[Client]: Enter server message passcode to decrypt: ").strip()
            if not authenticate_message(server_message_passcode):
                print("[Client]: Incorrect passcode. Cannot decrypt server's message.")
                continue

            # Extract the IV and encrypted data for decryption
            iv = encrypted_response[:16]
            encrypted_data = encrypted_response[16:]
            decrypted_message = decrypt_message(encrypted_data, server_message_passcode, iv)
            print(f"[Client]: Decrypted message from server: {decrypted_message}")

    except Exception as e:
        print(f"[Client]: Error during communication with server: {e}")
    finally:
        server_socket.close()
        print("[Client]: Connection to server closed.")