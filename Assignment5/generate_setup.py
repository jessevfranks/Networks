#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    NETWORK DEBUGGING LAB - SETUP GENERATOR                    ║
║                                                                                ║
║  This script generates your personalized lab environment with THREE           ║
║  difficulty levels, each in its own folder.                                  ║
║                                                                                ║
║  Usage:                                                                       ║
║    python3 generate_setup.py --username YOUR_LASTNAME                        ║
║                                                                                ║
║  This creates:                                                                ║
║    lab-easy/      - Level 1: Starter challenges                              ║
║    lab-medium/    - Level 2: More complex issues                             ║
║    lab-hard/      - Level 3: Advanced debugging                              ║
║                                                                                ║
║  Each folder is independent - work on any difficulty without affecting       ║
║  your progress in other levels!                                              ║
║                                                                                ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import re
import sys
import random
import argparse
from pathlib import Path
from textwrap import dedent


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def sanitize_username(username: str) -> str:
    """Convert username to Docker-friendly slug."""
    username = username.strip().lower()
    username = re.sub(r'[^a-z0-9._-]', '-', username)
    username = re.sub(r'[-._]+', lambda m: m.group(0)[0], username)
    if not re.match(r'^[a-z0-9]', username):
        username = f"u-{username}"
    return username[:32]


def print_banner(text: str) -> None:
    print("\n" + "═" * 60)
    print(f"  {text}")
    print("═" * 60)


def print_success(text: str) -> None:
    print(f"  ✓ {text}")


def print_info(text: str) -> None:
    print(f"  ℹ {text}")


def generate_random_ip(subnet_prefix: str, exclude: list = None) -> str:
    """Generate a random IP in the given subnet."""
    exclude = exclude or []
    while True:
        host = random.randint(10, 250)
        ip = f"{subnet_prefix}.{host}"
        if ip not in exclude:
            return ip


def generate_random_port(range_start: int = 8000, range_end: int = 9000) -> int:
    """Generate a random port number."""
    return random.randint(range_start, range_end)


# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

def generate_network_config(username: str, difficulty: str) -> dict:
    """Generate randomized network configuration."""
    # Use username + difficulty as seed for reproducible configs
    random.seed(hash(f"{username}-{difficulty}") % (2**32))
    
    # Generate random subnets
    frontend_second_octet = random.randint(16, 30)
    backend_second_octet = random.randint(31, 45)
    
    frontend_prefix = f"172.{frontend_second_octet}.0"
    backend_prefix = f"172.{backend_second_octet}.0"
    
    # Generate random IPs
    server_ip = generate_random_ip(backend_prefix)
    proxy_backend_ip = generate_random_ip(backend_prefix, [server_ip])
    proxy_frontend_ip = generate_random_ip(frontend_prefix)
    client_ip = generate_random_ip(frontend_prefix, [proxy_frontend_ip])
    
    # Generate random port
    app_port = generate_random_port()
    
    random.seed()
    
    return {
        'frontend_subnet': f"{frontend_prefix}.0/24",
        'frontend_gateway': f"{frontend_prefix}.1",
        'backend_subnet': f"{backend_prefix}.0/24",
        'backend_gateway': f"{backend_prefix}.1",
        'server_ip': server_ip,
        'proxy_frontend_ip': proxy_frontend_ip,
        'proxy_backend_ip': proxy_backend_ip,
        'client_ip': client_ip,
        'app_port': app_port,
        'frontend_prefix': frontend_prefix,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# DIFFICULTY CONFIGURATIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_easy_config(net_config: dict) -> dict:
   
    port = net_config['app_port'] + random.randint(100, 500)
    return {
        'client_env': {
            'PROXY_HOST': 'proxy',
            'PROXY_PORT': str(port),
        },
        'proxy_env': {
            'PROXY_PORT': str(net_config['app_port']),
            'SERVER_HOST': 'server',
            'SERVER_PORT': str(net_config['app_port']),
        },
        'server_env': {
            'APP_PORT': str(net_config['app_port']),
        },
        'proxy_entrypoint_extra': '',
        'client_entrypoint_extra': '',
        'proxy_cap_add': False,
        'client_cap_add': False,
        'frontend_mtu': 1500,
        'backend_mtu': 1500,
    }


def get_medium_config(net_config: dict) -> dict:
    
    return {
        'client_env': {
            'PROXY_HOST': 'proxy-server',
            'PROXY_PORT': str(net_config['app_port']),
        },
        'proxy_env': {
            'PROXY_PORT': str(net_config['app_port']),
            'SERVER_HOST': 'server',
            'SERVER_PORT': str(net_config['app_port']),
        },
        'server_env': {
            'APP_PORT': str(net_config['app_port']),
        },
        'proxy_entrypoint_extra': f"iptables -A OUTPUT -p tcp --dport {net_config['app_port']} -j DROP;",
        'client_entrypoint_extra': '',
        'proxy_cap_add': True,
        'client_cap_add': False,
        'frontend_mtu': 1500,
        'backend_mtu': 1500,
    }


def get_hard_config(net_config: dict) -> dict:
   
    gateway = f"{net_config['frontend_prefix']}.254"
    return {
        'client_env': {
            'PROXY_HOST': 'proxy-server',
            'PROXY_PORT': str(net_config['app_port']),
        },
        'proxy_env': {
            'PROXY_PORT': str(net_config['app_port']),
            'SERVER_HOST': 'server',
            'SERVER_PORT': str(net_config['app_port']),
        },
        'server_env': {
            'APP_PORT': str(net_config['app_port']),
        },
        'proxy_entrypoint_extra': f"iptables -A OUTPUT -p tcp --dport {net_config['app_port']} -j DROP;",
        'client_entrypoint_extra': f'ip route del default 2>/dev/null || true; ip route add default via {gateway};',
        'proxy_cap_add': True,
        'client_cap_add': True,
        'frontend_mtu': 1500,
        'backend_mtu': 1400,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER COMPOSE GENERATION
# ═══════════════════════════════════════════════════════════════════════════════

def generate_compose(username: str, user_slug: str, difficulty: str, net_config: dict, config: dict) -> str:
    """Generate docker-compose.yml content."""
    
    client_env = '\n'.join([f"      - {k}={v}" for k, v in config['client_env'].items()])
    proxy_env = '\n'.join([f"      - {k}={v}" for k, v in config['proxy_env'].items()])
    server_env = '\n'.join([f"      - {k}={v}" for k, v in config['server_env'].items()])
    
    base_packages = "apt-get update -qq && apt-get install -y -qq iputils-ping netcat-openbsd tcpdump iproute2 dnsutils"
    
    proxy_entrypoint = f'{base_packages} iptables > /dev/null 2>&1; {config.get("proxy_entrypoint_extra", "")} exec bash'
    client_entrypoint = f'{base_packages} > /dev/null 2>&1; {config.get("client_entrypoint_extra", "")} exec bash'
    server_entrypoint = f'{base_packages} > /dev/null 2>&1; exec bash'
    
    proxy_cap = "    cap_add:\n      - NET_ADMIN" if config.get('proxy_cap_add') else ""
    client_cap = "    cap_add:\n      - NET_ADMIN" if config.get('client_cap_add') else ""
    
    return f'''# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK DEBUGGING LAB - {difficulty.upper()}
# Generated for: {username}
# ═══════════════════════════════════════════════════════════════════════════════
#
# Your mission: Get the client talking to the server through the proxy!
#
# TO START:
#   docker compose up -d
#   docker compose exec server bash
#   docker compose exec proxy bash
#   docker compose exec client bash
#
# ═══════════════════════════════════════════════════════════════════════════════

version: "3.9"

services:
  server:
    image: python:3.11-slim
    container_name: {difficulty}-server-{user_slug}
    hostname: server
    working_dir: /app
    volumes:
      - ./server:/app
    environment:
      - STUDENT_USERNAME={username}
{server_env}
    command: bash
    tty: true
    stdin_open: true
    networks:
      backend_net:
        ipv4_address: {net_config['server_ip']}
    entrypoint: >
      bash -c "{server_entrypoint}"

  proxy:
    image: python:3.11-slim
    container_name: {difficulty}-proxy-{user_slug}
    hostname: proxy
    working_dir: /app
    volumes:
      - ./proxy:/app
    environment:
      - STUDENT_USERNAME={username}
{proxy_env}
    command: bash
    tty: true
    stdin_open: true
{proxy_cap}
    networks:
      frontend_net:
        ipv4_address: {net_config['proxy_frontend_ip']}
      backend_net:
        ipv4_address: {net_config['proxy_backend_ip']}
    depends_on:
      - server
    entrypoint: >
      bash -c "{proxy_entrypoint}"

  client:
    image: python:3.11-slim
    container_name: {difficulty}-client-{user_slug}
    hostname: client
    working_dir: /app
    volumes:
      - ./client:/app
    environment:
      - STUDENT_USERNAME={username}
{client_env}
    command: bash
    tty: true
    stdin_open: true
{client_cap}
    networks:
      frontend_net:
        ipv4_address: {net_config['client_ip']}
    depends_on:
      - proxy
    entrypoint: >
      bash -c "{client_entrypoint}"

networks:
  frontend_net:
    driver: bridge
    ipam:
      config:
        - subnet: {net_config['frontend_subnet']}
          gateway: {net_config['frontend_gateway']}
    driver_opts:
      com.docker.network.driver.mtu: {config['frontend_mtu']}

  backend_net:
    driver: bridge
    ipam:
      config:
        - subnet: {net_config['backend_subnet']}
          gateway: {net_config['backend_gateway']}
    driver_opts:
      com.docker.network.driver.mtu: {config['backend_mtu']}
'''


# ═══════════════════════════════════════════════════════════════════════════════
# CODE TEMPLATES
# ═══════════════════════════════════════════════════════════════════════════════

STARTER_SERVER = '''#!/usr/bin/env python3
"""
TCP Echo Server

Your server should:
  1. Bind to the correct interface and port
  2. Listen for incoming connections
  3. Accept connections and echo back received data
  4. Handle client disconnections gracefully

TODO: Fill in HOST and PORT values by examining your environment!
"""

import os
import sys
import socket
from typing import Tuple

USERNAME = os.getenv("STUDENT_USERNAME", "student")

# TODO: Determine the correct values for HOST and PORT
# Hint: Use 'env' command inside the container to see environment variables
# Hint: Think about what address allows connections from other containers
HOST = None  # What address should the server bind to?
PORT = None  # What port should the server listen on?

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
            print("\\n[server] Shutting down.")
            break
    
    sock.close()


if __name__ == "__main__":
    main()
'''

STARTER_CLIENT = '''#!/usr/bin/env python3
"""
TCP Echo Client

Your client should:
  1. Connect to the proxy server
  2. Send user input as messages
  3. Receive and display the echoed response
  4. Handle errors gracefully

TODO: Fill in PROXY_HOST and PROXY_PORT values by examining your environment!
"""

import os
import sys
import socket
import time

USERNAME = os.getenv("STUDENT_USERNAME", "student")

# TODO: Determine the correct values for PROXY_HOST and PROXY_PORT
# Hint: Use 'env' command inside the container to see environment variables
# Hint: The client connects to the PROXY, not directly to the server
PROXY_HOST = None  # What is the proxy hostname?
PROXY_PORT = None  # What port is the proxy listening on?

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
        print("\\n[client] Exiting.")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
'''

STARTER_PROXY = '''#!/usr/bin/env python3
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
            print("\\n[proxy] Shutting down.")
            break
    
    sock.close()


if __name__ == "__main__":
    main()
'''


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Generate personalized debugging lab with all difficulty levels",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent('''
        Example:
          python3 generate_setup.py --username smith
          
        This creates three independent folders:
          lab-easy/     - Start here!
          lab-medium/   - More challenging
          lab-hard/     - Expert level
        ''')
    )
    parser.add_argument("--username", "-u", required=True, help="Your last name")
    
    args = parser.parse_args()
    
    username = args.username
    user_slug = sanitize_username(username)
    
    print_banner("NETWORK DEBUGGING LAB SETUP")
    print(f"  Username: {username}")
    print(f"  Creating all three difficulty levels...")
    
    difficulties = [
        ('easy', get_easy_config),
        ('medium', get_medium_config),
        ('hard', get_hard_config),
    ]
    
    for difficulty, config_func in difficulties:
        print_banner(f"Creating lab-{difficulty}/")
        
        # Create directory structure
        lab_dir = Path(f"lab-{difficulty}")
        server_dir = lab_dir / "server"
        proxy_dir = lab_dir / "proxy"
        client_dir = lab_dir / "client"
        
        for d in [server_dir, proxy_dir, client_dir]:
            d.mkdir(parents=True, exist_ok=True)
        
        # Generate network config
        net_config = generate_network_config(username, difficulty)
        config = config_func(net_config)
        
        # Write docker-compose.yml
        compose = generate_compose(username, user_slug, difficulty, net_config, config)
        (lab_dir / "docker-compose.yml").write_text(compose, encoding="utf-8")
        print_success("docker-compose.yml")
        
        # Write code files
        (server_dir / "server.py").write_text(STARTER_SERVER, encoding="utf-8")
        print_success("server/server.py")
        
        (client_dir / "client.py").write_text(STARTER_CLIENT, encoding="utf-8")
        print_success("client/client.py")
        
        (proxy_dir / "proxy.py").write_text(STARTER_PROXY, encoding="utf-8")
        print_success("proxy/proxy.py")
        
        print_info(f"Network: {net_config['frontend_subnet']} <-> {net_config['backend_subnet']}")
        print_info(f"App Port: {net_config['app_port']}")
    
    print_banner("SETUP COMPLETE")
    print('''
  Three independent lab environments created:
  
    lab-easy/      Start here! Basic configuration issues.
    lab-medium/    Adds network-level challenges.
    lab-hard/      Multiple cascading problems.
  
  To work on a difficulty level:
  
    cd lab-easy
    docker compose up -d
    docker compose exec server bash
    docker compose exec proxy bash
    docker compose exec client bash
  
  Each folder is independent - your progress in one
  does not affect the others. Good luck! 🔍
''')


if __name__ == "__main__":
    main()
