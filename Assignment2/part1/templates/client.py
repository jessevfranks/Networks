"""
TCP Echo Client (Docker-friendly) — INCOMPLETE SKELETON

Goals for students:
- Connect to server name/port from env (Docker DNS)
- Read user input; prepend username; send bytes; receive echo
- Observe cleartext payloads in Wireshark on your assigned ports
- Handle errors & clean shutdown

Fill every TODO.
"""

import os
import socket
import sys
import time

USERNAME = os.getenv("STUDENT_USERNAME") or "FILL_ME"

## Fill the correct host and IP detail from the docker compose file or output from helper script file
SERVER_HOST = None
SERVER_PORT = None  

CONNECT_TIMEOUT = 5  # seconds


def connect_once(host: str, port: int) -> socket.socket:
    """Create a TCP connection to the server."""
    if port is None:
        raise ValueError("SERVER_PORT is not set. Provide via env or set a default.")
    # TODO: choose API: socket.create_connection or manual socket + connect
    pass


def main() -> None:
    print(f"[client:{USERNAME}] target → {SERVER_HOST}:{SERVER_PORT}")
    try:
        sock = connect_once(SERVER_HOST, SERVER_PORT)
    except Exception as e:
        print(f"[client:{USERNAME}] connection failed: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[client:{USERNAME}] connected. Type messages; Ctrl+C to quit.")
    try:
        while True:
            # TODO: get input from user to send it to server

            # TODO: send data
        

            # TODO: receive response from server and print it
           

            # OPTIONAL: small delay to make captures easier to read
            time.sleep(0.1)

            break  # TODO: remove this break to keep the loop going
    except KeyboardInterrupt:
        print("\n[client] exiting.")
    except Exception as e:
        print(f"[client:{USERNAME}] error: {e}", file=sys.stderr)
    finally:
        try:
            sock.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
