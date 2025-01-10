import socket
from Authentication.authentication import authenticate_client, authenticate_message
from CryptoOperations.encryption import encrypt_message
from CryptoOperations.decryption import decrypt_message

def handle_client(client_socket, client_address, all_clients):
    try:
        # Step 1: Receive passcode from client
        print(f"[Server]: Waiting for client {client_address} to authenticate.")
        client_passcode = client_socket.recv(1024).decode('utf-8')
        if not client_passcode:
            print(f"[Server]: Client {client_address} disconnected before sending passcode.")
            return

        # Step 2: Authenticate client
        if authenticate_client(client_passcode):
            client_socket.send("Authentication successful.".encode('utf-8'))
            print(f"[Server]: Client {client_address} authenticated successfully.")
        else:
            client_socket.send("Authentication failed.".encode('utf-8'))
            print(f"[Server]: Client {client_address} failed authentication.")
            client_socket.close()
            return

        # Step 3: Communication loop
        while True:
            # Step 4: Receive encrypted message
            encrypted_message = client_socket.recv(4096)
            if not encrypted_message:
                print(f"[Server]: Client {client_address} disconnected.")
                break
            
            iv = encrypted_message[:16]
            encrypted_data = encrypted_message[16:]

            # Step 5: Decrypt received message
            try:
                sender_message_passcode = input("[Server]: Enter client's message passcode to decrypt: ").strip()
                if not authenticate_message(sender_message_passcode):
                    print("[Server]: Incorrect message passcode. Message remains encrypted.")
                    continue

                decrypted_message = decrypt_message(encrypted_data, sender_message_passcode)
                print(f"[Server]: Decrypted message from {client_address}: {decrypted_message}")

                # Step 6: Respond with an encrypted message
                response_message = input("[Server]: Enter response to client: ")
                encrypted_response = encrypt_message(response_message, "mymessagepasscode")  # Server's passcode
                client_socket.send(encrypted_response)
                print(f"[Server]: Encrypted response sent to {client_address}.")

            except Exception as e:
                print(f"[Server]: Error during message handling: {e}")
                break

    except Exception as e:
        print(f"[Server]: An error occurred with client {client_address}: {e}")
    finally:
        if client_socket in all_clients:
            all_clients.remove(client_socket)
        client_socket.close()
        print(f"[Server]: Connection with {client_address} closed.")
