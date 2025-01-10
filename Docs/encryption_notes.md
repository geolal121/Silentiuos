# Encryption Notes

## Overview of Encryption

Encryption is a core feature of **Silentious**. It ensures that all messages sent between clients are private and cannot be read by anyone other than the intended recipient. In Silentious, we use **AES encryption** (Advanced Encryption Standard) to encrypt and decrypt messages.

### Why Encryption is Important:
- **Privacy**: Ensures that no unauthorized user can read the messages.
- **Security**: Protects against interception or man-in-the-middle attacks.
- **Confidentiality**: Guarantees that only the recipient with the correct key can read the message content.

## Encryption Algorithm: AES (Advanced Encryption Standard)

**AES** is a symmetric encryption algorithm, meaning the same key is used to encrypt and decrypt messages. In Silentious, we use AES with a **128-bit key size** for encrypting messages. This level of encryption is both secure and efficient.

### AES Workflow:
1. **Encryption**:
   - The sender encrypts the message using their passcode as the encryption key.
   - The message is encrypted before being sent to the server.
   
2. **Decryption**:
   - The recipient uses the same passcode to decrypt the message.
   - The decrypted message is then displayed in the client interface.

AES is widely considered to be secure and is used in many systems requiring high levels of data protection.

## Key Management

In Silentious, the **passcode** serves as the key for encryption and decryption. The passcode is shared between the sender and the recipient, and it is never stored on the server. This ensures that no one (including the server) can read the messages.

### Key Storage:
- The passcode is never stored in plaintext anywhere. It is only used during the encryption/decryption process.
- The passcode is never transmitted over the network in plaintext; instead, it is used to generate an encryption key.

### Security Considerations:
- **Passcode Protection**: Users must protect their passcode as it is the key to decrypting their messages.
- **Key Generation**: A secure method of generating the key (e.g., using a hash function) can ensure that the passcode isn't exposed.

## Additional Security Notes

While AES is a highly secure encryption method, the overall security of Silentious depends on how securely the passcode is handled. Here are a few tips to improve security:

1. **Use Strong Passcodes**: Ensure that your passcode is complex and not easily guessable.
2. **Secure Your Device**: Keep your device protected with encryption, strong passwords, and other security measures to prevent unauthorized access to your messages.
3. **Avoid Sharing Passcodes**: Share passcodes only with trusted individuals and never over insecure channels.
4. **Use TLS/SSL**: For added security, especially over public networks, consider implementing **TLS/SSL** encryption to secure the connection between the client and server.