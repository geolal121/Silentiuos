## How to Use Silentious

After setting up **Silentious**, follow these steps to send and receive encrypted messages:

### 1. Connect to the Server:
   - Once the server is running, launch the **client**.
   - You will be prompted to enter the **server IP address** and the **passcode** to authenticate.
   - The passcode is used to verify your identity and ensure secure communication.
   - Upon successful authentication, you will be connected to the server.

### 2. Sending a Message:
   - Once connected, you can type a message in the client interface.
   - The client will **encrypt** the message using **AES encryption** before sending it to the server.
   - The encrypted message is then routed through the server to the recipient.

### 3. Receiving a Message:
   - When a new message is received, the client will display the **encrypted message**.
   - The message will be decrypted using the **passcode** (which both the sender and recipient know).
   - The decrypted message will be shown in the client interface.

### 4. Real-Time Communication:
   - The client will continuously check for incoming messages from the server.
   - Messages are delivered instantly, and the interface will automatically update with the new messages in real-time.

### 5. End-to-End Security:
   - All messages are encrypted before they leave your device and are only decrypted when received by the intended recipient.
   - The server does **not decrypt** the messages, ensuring that only you and the recipient have access to the content.

### 6. Disconnecting:
   - To disconnect, simply close the client application. The server will stop accepting new connections once the client disconnects.

### Example:
1. **Start the server** on one machine.
2. **Start the client** on another machine and enter the server’s **IP address** and **passcode**.
3. Type and send a message to the other user. The message will be encrypted and displayed once decrypted on the recipient’s side.