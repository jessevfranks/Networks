import socket


def run_server():
    # 1. Create a socket
    # AF_INET = IPv4, SOCK_DGRAM = UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 2. Bind to an address and port
    # 'localhost' (or 127.0.0.1) means it only accepts local connections.
    # To accept connections from outside (like a real VM), use '0.0.0.0'.
    server_address = ('localhost', 12345)
    print(f"Starting UDP Server on {server_address[0]} port {server_address[1]}...")
    server_socket.bind(server_address)

    while True:
        print("\nWaiting for message...")

        # 3. Receive data
        # recvfrom returns the data and the address of the sender
        data, address = server_socket.recvfrom(4096)

        print(f"Received {len(data)} bytes from {address}")
        print(f"Message content: {data.decode('utf-8')}")

        # 4. Send a reply (optional, but good for confirmation)
        if data:
            server_socket.sendto(b"Message received!", address)


if __name__ == "__main__":
    try:
        run_server()
    except KeyboardInterrupt:
        print("\nServer stopping...")