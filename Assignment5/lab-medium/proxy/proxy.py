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

LISTEN_PORT = 8275  # What port should the proxy listen on?
SERVER_HOST = "server"  # What is the backend server's hostname?
SERVER_PORT = 8275 # What port is the backend server listening on?

BUFFER_SIZE = 4096


def create_listen_socket() -> socket.socket:
    """Create the listening socket for client connections."""
    if LISTEN_PORT is None:
        raise ValueError("LISTEN_PORT not configured!")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((LISTEN_HOST, LISTEN_PORT))

    sock.listen(5)
    
    print(f"[proxy:{USERNAME}] Listening on {LISTEN_HOST}:{LISTEN_PORT}")
    return sock


def handle_connection(client_sock: socket.socket, client_addr: tuple) -> None:
    """Relay data between client and backend server."""
    print(f"[proxy:{USERNAME}] Client connected: {client_addr}")
    
    if SERVER_HOST is None or SERVER_PORT is None:
        print("[proxy] ERROR: Backend server not configured!")
        client_sock.close()
        return

    server_sock = socket.create_connection((SERVER_HOST, SERVER_PORT), timeout=10)
    
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
                    data = sock.recv(BUFFER_SIZE)
                    
                    if not data:
                        raise ConnectionError("Client disconnected")
                    
                    server_sock.sendall(data)
                    
                    print(f"[proxy] CLIENT -> SERVER: {len(data)} bytes")
                    
                elif sock is server_sock:
                    data = sock.recv(BUFFER_SIZE)
                    
                    if not data:
                        raise ConnectionError("Server disconnected")
                    
                    sock.sendall(data)
                    
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
            client_sock, client_addr = sock.accept()
            
            if client_sock:
                handle_connection(client_sock, client_addr)
                
        except KeyboardInterrupt:
            print("\n[proxy] Shutting down.")
            break
    
    sock.close()


if __name__ == "__main__":
    main()
