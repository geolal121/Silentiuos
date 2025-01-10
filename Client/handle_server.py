from Authentication.authentication import authenticate_message
from CryptoOperations.encryption import encrypt_message
from CryptoOperations.decryption import decrypt_message

def handle_server(server_socket):
    try:
        # Step 1: Communicate loop
        while True:
            message = input("[Client]: Enter your message (or type 'exit' to quit): ")
            if message.lower() == 'exit':
                print("[Client]: Exiting chat...")
                break

            encrypt_message = encrypt_message(message, "mypmessagepasscode")
            server_socket.send(encrypt_message)
            print("[Client]: Encrypted message sent to server.")

            print("[Client]: Waiting for server response...")
            encypted_response = server_socket.recv(4096)
            if not encypted_response:
                print("[Client]: Server has disconnected.")
                break

            iv = encypted_response[:16]
            encrypted_data = encypted_response[16:]

            server_message_passcode = input("[Client]: Enter server message passcode to decrypt: ").strip()
            if not authenticate_message(server_message_passcode):
                print("[Client]: Incorrect passcode. Cannot decrypt server's message.")
                continue

            decrypted_message = decrypt_message(encrypted_data, server_message_passcode, iv)
            print(f"[Client]: Decrypted message from server: {decrypted_message}")
    
    except Exception as e:
        print(f"[Client]: Error during communication with server: {e}")
    finally:
        server_socket.close()
        print("[Client]: Connection to server closed.")