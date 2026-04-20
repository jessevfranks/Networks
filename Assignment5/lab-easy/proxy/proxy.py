#!/usr/bin/env python3
"""
TCP Proxy - Complete the TODOs to relay traffic between client and server!

Your proxy should:
  1. Listen for client connections on the frontend network
  2. Connect to the backend server for each client
  3. Relay data bidirectionally between client and server
  4. Handle disconnections gracefully

Architecture:
  Client --[frontend_net]--> PROXY --[backend_net]--> Server
"""

import os
import sys
import socket
import select

USERNAME = os.getenv("STUDENT_USERNAME", "student")

# The proxy listens on all interfaces
LISTEN_HOST = "0.0.0.0"

# TODO: Read configuration from environment variables
# Hint: Use 'env' command inside the container to see what's available
LISTEN_PORT = None  # What port should the proxy listen on?
SERVER_HOST = None  # What is the backend server's hostname?
SERVER_PORT = None  # What port is the backend server listening on?

BUFFER_SIZE = 4096


def create_listen_socket() -> socket.socket:
    """Create the listening socket for client connections."""
    if LISTEN_PORT is None:
        raise ValueError("LISTEN_PORT not configured!")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # TODO: Bind the socket to (LISTEN_HOST, LISTEN_PORT)
    
    # TODO: Start listening for connections (backlog of 5 is fine)
    
    print(f"[proxy:{USERNAME}] Listening on {LISTEN_HOST}:{LISTEN_PORT}")
    return sock


def handle_connection(client_sock: socket.socket, client_addr: tuple) -> None:
    """Relay data between client and backend server."""
    print(f"[proxy:{USERNAME}] Client connected: {client_addr}")
    
    if SERVER_HOST is None or SERVER_PORT is None:
        print("[proxy] ERROR: Backend server not configured!")
        client_sock.close()
        return
    
    # TODO: Connect to the backend server
    server_sock = None
    
    if server_sock is None:
        print("[proxy] ERROR: Server connection not implemented!")
        client_sock.close()
        return
    
    print(f"[proxy:{USERNAME}] Relay: {client_addr} <-> {SERVER_HOST}:{SERVER_PORT}")
    
    # Set non-blocking for select()
    client_sock.setblocking(False)
    server_sock.setblocking(False)
    
    sockets = [client_sock, server_sock]
    
    try:
        while True:
            readable, _, _ = select.select(sockets, [], sockets, 1.0)
            
            for sock in readable:
                if sock is client_sock:
                    # TODO: Receive data from client
                    data = None
                    
                    if not data:
                        raise ConnectionError("Client disconnected")
                    
                    # TODO: Forward data to server
                    
                    print(f"[proxy] CLIENT -> SERVER: {len(data)} bytes")
                    
                elif sock is server_sock:
                    # TODO: Receive data from server
                    data = None
                    
                    if not data:
                        raise ConnectionError("Server disconnected")
                    
                    # TODO: Forward data to client
                    
                    print(f"[proxy] SERVER -> CLIENT: {len(data)} bytes")
                    
    except Exception as e:
        print(f"[proxy:{USERNAME}] Session ended: {e}")
    finally:
        client_sock.close()
        server_sock.close()
        print(f"[proxy:{USERNAME}] Connection closed: {client_addr}")


def main():
    try:
        sock = create_listen_socket()
    except Exception as e:
        print(f"[proxy:{USERNAME}] Failed to start: {e}")
        sys.exit(1)
    
    while True:
        try:
            # TODO: Accept incoming connection
            
            client_sock, client_addr = None, None
            
            if client_sock:
                handle_connection(client_sock, client_addr)
                
        except KeyboardInterrupt:
            print("\n[proxy] Shutting down.")
            break
    
    sock.close()


if __name__ == "__main__":
    main()
