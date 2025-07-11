import socket

# Server address and port
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

def receive_messages():
    # Create UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Bind to server address and port
        sock.bind((SERVER_IP, SERVER_PORT))
        print(f"Listening on {SERVER_IP}:{SERVER_PORT}")
        
        while True:
            # Receive message from client
            message_bytes, addr = sock.recvfrom(1024)
            # Decode bytes to string
            message = message_bytes.decode('ascii')
            print(f"Received: {message}")
            if message.lower() == 'exit':
                print("Exiting...")
                break

if __name__ == "__main__":
    receive_messages()
