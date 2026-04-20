#!/usr/bin/env python3
"""
TCP Echo Server

Your server should:
  1. Bind to the correct interface and port
  2. Listen for incoming connections
  3. Accept connections and echo back received data
  4. Handle client disconnections gracefully
"""

import os
import sys
import socket
from typing import Tuple

USERNAME = os.getenv("STUDENT_USERNAME", "student")

HOST = "proxy"  # What address should the server bind to?
PORT = 8275  # What port should the server listen on?

BUFFER_SIZE = 4096


def create_listen_socket(host: str, port: int) -> socket.socket:
    """Create, bind, and listen on a TCP socket."""
    if host is None or port is None:
        raise ValueError("HOST and PORT must be configured!")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    sock.bind((host, port))
    sock.listen(5)
    
    print(f"[server:{USERNAME}] Listening on {host}:{port}")
    return sock


def handle_client(conn: socket.socket, addr: Tuple[str, int]) -> None:
    """Handle a single client connection - receive and echo data."""
    print(f"[server:{USERNAME}] Connection from {addr}")
    
    try:
        while True:
            data = conn.recv(BUFFER_SIZE)
            
            if not data:
                break
            
            print(f"[server:{USERNAME}] Received: {data!r}")
            
            response = f"[ECHO from {USERNAME}] {data.decode()}".encode()
            conn.sendall(response)
            
    except Exception as e:
        print(f"[server:{USERNAME}] Error: {e}")
    finally:
        conn.close()
        print(f"[server:{USERNAME}] Connection closed: {addr}")


def main():
    try:
        sock = create_listen_socket(HOST, PORT)
    except Exception as e:
        print(f"[server:{USERNAME}] Failed to start: {e}")
        sys.exit(1)
    
    while True:
        try:
            conn, addr = sock.accept()
            handle_client(conn, addr)
                
        except KeyboardInterrupt:
            print("\n[server] Shutting down.")
            break
    
    sock.close()


if __name__ == "__main__":
    main()
