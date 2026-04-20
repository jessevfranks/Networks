#!/usr/bin/env python3
"""
TCP Echo Client

Your client should:
  1. Connect to the proxy server
  2. Send user input as messages
  3. Receive and display the echoed response
  4. Handle errors gracefully
"""

import os
import sys
import socket
import time

USERNAME = os.getenv("STUDENT_USERNAME", "student")

PROXY_HOST = "proxy"  # What is the proxy hostname?
PROXY_PORT = 8275  # What port is the proxy listening on?

BUFFER_SIZE = 4096


def main():
    print(f"[client:{USERNAME}] Target: {PROXY_HOST}:{PROXY_PORT}")
    
    if PROXY_HOST is None or PROXY_PORT is None:
        print("[client] ERROR: Connection settings not configured!")
        print("[client] Hint: Check environment variables with 'env' command")
        sys.exit(1)
    
    try:
        sock = socket.create_connection((PROXY_HOST, PROXY_PORT), timeout=10)
    except Exception as e:
        print(f"[client:{USERNAME}] Connection failed: {e}")
        sys.exit(1)
    
    print(f"[client:{USERNAME}] Connected! Type messages (Ctrl+C to quit)")
    
    try:
        while True:
            msg = input(f"[{USERNAME}]> ")
            
            if msg.lower() in ('quit', 'exit'):
                break
            
            if not msg.strip():
                continue
            
            full_msg = f"[{USERNAME}] {msg}"
            sock.sendall(full_msg.encode())
            
            response = sock.recv(BUFFER_SIZE)
            if response:
                print(f"  <- {response.decode()}")
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n[client] Exiting.")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
