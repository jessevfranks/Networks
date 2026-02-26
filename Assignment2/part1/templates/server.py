"""
TCP Echo Server Template

Goals for students:
- Bind to the correct interface/port (from env)
- Accept connections in a loop
- Read bytes; echo back; log messages with your username
- Gracefully handle disconnects and errors

Fill every TODO. Don't copy/paste a finished server.
"""

import os
import socket
import sys
from typing import Tuple


USERNAME = os.getenv("STUDENT_USERNAME") # <-- put your username (or ensure env is set)
HOST = "0.0.0.0"  # listen on all interfaces in container
PORT = None  #TODO: Fill the correct port obtained from the docker compose file or output from helper script file


def create_listen_socket(host: str, port: int) -> socket.socket:
    """Create, bind, and listen on a TCP socket."""
    if port is None:
        raise ValueError("PORT is not set. Provide APP_PORT via env or hardcode it for learning.")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # TODO: bind the socket using host IP and port address
    # s.bind((..., ...))
    # TODO: start listening on the bound socket (backlog can be 1 or more)
    # s.listen(...)
    return s


def handle_client(conn: socket.socket, addr: Tuple[str, int]) -> None:
    """Echo loop for a single client."""
    print(f"[server:{USERNAME}] connection from {addr}")

    while True:
        
        data = None ## TODO: Modify to receive data from client (choose a buffer size, e.g., 4096)
      
        if not data: 
            break
        
        print(f"[server:{USERNAME}] received: {data!r}")
        # TODO: echo customized message back to client
 


def main() -> None: 
    try:
        lsock = create_listen_socket(HOST, PORT)
    except Exception as e:
        print(f"[server:{USERNAME}] failed to create listen socket: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[server:{USERNAME}] listening on {HOST}:{PORT}")
    while True:
        try:
            # TODO: accept a connection and handle the client
       
            conn, addr = None, None  # TODO: replace with actual accept call
        except KeyboardInterrupt:
            print("\n[server] shutting down (KeyboardInterrupt).")
            break
        except Exception as e:
            print(f"[server:{USERNAME}] error: {e}", file=sys.stderr)

    # TODO: close listening socket


if __name__ == "__main__":
    main()