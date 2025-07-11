import socket

# Server address and port
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

def send_message(message):
    # Create UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Encode message to bytes
        message_bytes = message.encode('ascii')
        # Send message to server
        print(message_bytes)
        sock.sendto(message_bytes, (SERVER_IP, SERVER_PORT))
        print(f"Sent: {message}")

if __name__ == "__main__":
    while True:
        msg = input("Enter message to send (or 'exit' to quit): ")
        if msg.lower() == 'exit':
            break
        send_message(msg)
