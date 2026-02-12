import socket


def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('localhost', 12345)
    message = "New message"

    try:
        # 2. Send data
        print(f"Sending: '{message}'")
        client_socket.sendto(message.encode('utf-8'), server_address)

        try:
            data, server = client_socket.recvfrom(4096)
            print(f"Received from server: {data.decode('utf-8')}")
        except socket.timeout:
            print("Request timed out. The server might be down or packet lost.")

    finally:
        print("Closing socket")
        client_socket.close()


if __name__ == "__main__":
    run_client()