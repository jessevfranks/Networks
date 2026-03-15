"""
TCP Echo Server Template

Goals for students:
- Bind to the correct interface/port (from env)
- Accept connections in a loop
- Read bytes; echo back; log messages with your username
- Gracefully handle disconnects and errors
"""

import os
import socket
import sys
from typing import Tuple


USERNAME = os.getenv("STUDENT_USERNAME") # <-- put your username (or ensure env is set)
HOST = "0.0.0.0"  # listen on all interfaces in container
PORT = 8084 # port from docker compose


def create_listen_socket(host: str, port: int) -> socket.socket:
    """Create, bind, and listen on a TCP socket."""
    if port is None:
        raise ValueError("PORT is not set. Provide APP_PORT via env or hardcode it for learning.")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT)) # bind the socket to the server host/port
    s.listen(1) # listen on said port for a connection
    return s


def handle_client(conn: socket.socket, addr: Tuple[str, int]) -> None:
    """Echo loop for a single client."""
    print(f"[server:{USERNAME}] connection from {addr}")

    while True:
        
        data =  conn.recv(1024).decode() # receive and decode data from the client
      
        if not data: 
            break
        
        print(f"[server:{USERNAME}] received: {data!r}")
        conn.send(data.encode()) # send the received data back to the client
 


def main() -> None: 
    try:
        lsock = create_listen_socket(HOST, PORT)
    except Exception as e:
        print(f"[server:{USERNAME}] failed to create listen socket: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[server:{USERNAME}] listening on {HOST}:{PORT}")
    while True:
        try:
            conn, addr = lsock.accept() # accept a connection from a client, creating a connection and address object
            handle_client(conn, addr) # pass the above objects to our helper function to handle messages
        except KeyboardInterrupt:
            print("\n[server] shutting down (KeyboardInterrupt).")
            break
        except Exception as e:
            print(f"[server:{USERNAME}] error: {e}", file=sys.stderr)

    lsock.close() # close the socket at the end


if __name__ == "__main__":
    main()