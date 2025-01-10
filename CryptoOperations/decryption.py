from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def decrypt_message(encrypted_message, passcode, iv):
    """
    Decrypts an encrypted message using AES decryption and the passcode as the key.
    
    :param encrypted_message: The ciphertext (bytes) excluding the IV.
    :param passcode: The passcode (string) used as the key for decryption.
    :param iv: The initialization vector (16 bytes) used for decryption.
    :return: The decrypted plain-text message as a string.
    :raises ValueError: If decryption fails due to invalid input.
    """

    try:
        # Ensure the key is 16 bytes (128 bits) for AES-128
        key = passcode.ljust(16)[:16].encode('utf-8')
        
        # Validate IV size
        if len(iv) != 16:
            raise ValueError("Invalid IV size: must be 16 bytes.")

        # Create AES cipher object in CBC mode
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt the message
        decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()

        # Unpad the decrypted message (remove padding)
        pad_length = decrypted_message[-1]
        if pad_length > 16:
            raise ValueError("Invalid padding detected.")
        decrypted_message = decrypted_message[:-pad_length]

        # Convert bytes back to string and return
        return decrypted_message.decode('utf-8')

    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")
