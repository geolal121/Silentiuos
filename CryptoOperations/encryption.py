from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def encrypt_message(message, passcode):
    """
    Encrypts a message using AES encryption and the given passcode as the key.

    :param message: The plain-text message to encrypt (string).
    :param passcode: The passcode (string) used as the key for encryption.
    :return: The encrypted message in bytes, concatenated with the IV.
    :raises ValueError: If the message is empty or invalid.
    """

    try:
        # Ensure the key is 16 bytes (128 bits) for AES-128
        key = passcode.ljust(16)[:16].encode('utf-8')
        
        # Generate a random IV (16 bytes)
        iv = os.urandom(16)

        # Create AES cipher object in CBC mode
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Validate the message
        if not message:
            raise ValueError("The message cannot be empty.")

        # Pad the message to ensure it's a multiple of 16 bytes
        pad_length = 16 - len(message) % 16
        padded_message = message + chr(pad_length) * pad_length

        # Encrypt the padded message
        encrypted_message = encryptor.update(padded_message.encode('utf-8')) + encryptor.finalize()

        # Return the IV and encrypted message concatenated
        return iv + encrypted_message

    except Exception as e:
        raise ValueError(f"Encryption failed: {str(e)}")
