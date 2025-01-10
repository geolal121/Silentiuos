import unittest
from Authentication.authentication import authenticate_client, authenticate_message
from CryptoOperations.decryption import decrypt_message
from CryptoOperations.encryption import encrypt_message

class TestCryptoOperations(unittest.TestCase):
    def setUp(self):
        # Set up shared variables for tests
        self.valid_client_passcode = "mypasscode"
        self.invalid_client_passcode = "wrongpasscode"
        self.valid_message_passcode = "mymessagepasscode"
        self.invalid_message_passcode = "wrongmessagepasscode"
        self.test_message = "This is a test message."

    def test_encrypt_decrypt_correct_passcode(self):
        # Encrypt and then decrypt the message with the correct passcode
        encrypted_message = encrypt_message(self.test_message, self.valid_message_passcode)
        iv = encrypted_message[:16]  # Extract IV
        encrypted_data = encrypted_message[16:]  # Extract encrypted data
        decrypted_message = decrypt_message(encrypted_data, self.valid_message_passcode, iv)
        self.assertEqual(decrypted_message, self.test_message)

    def test_encrypt_decrypt_wrong_passcode(self):
        # Encrypt the message and attempt to decrypt it with the wrong passcode
        encrypted_message = encrypt_message(self.test_message, self.valid_message_passcode)
        iv = encrypted_message[:16]
        encrypted_data = encrypted_message[16:]
        with self.assertRaises(Exception):
            decrypt_message(encrypted_data, self.invalid_message_passcode, iv)

    def test_authenticate_client(self):
        # Test valid and invalid client passcodes
        self.assertTrue(authenticate_client(self.valid_client_passcode))
        self.assertFalse(authenticate_client(self.invalid_client_passcode))

    def test_authenticate_message(self):
        # Test valid and invalid message passcodes
        self.assertTrue(authenticate_message(self.valid_message_passcode))
        self.assertFalse(authenticate_message(self.invalid_message_passcode))

if __name__ == "__main__":
    unittest.main()