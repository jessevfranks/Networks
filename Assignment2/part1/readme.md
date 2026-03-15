## CSCI 4760 – Computer Networks Security
Assignment #2: Part I - TCP Networking + Wireshark

**Due: 3/5 at 11:59pm**

Overview
--------
In this assignment you will:

- Setup docker containers
- Implement a TCP echo client/server in Python
- Capture and analyze the traffic with Wireshark/tcpdump

Before you start (useful links)
- Docker (install): https://docs.docker.com/get-docker/
- Docker Compose / CLI: https://docs.docker.com/compose/cli-command/
- Wireshark (install): https://www.wireshark.org/download.html

Make sure to execute the following steps within the Linux VM. 


Generate the compose file (**1 Point**)
-------------------------
Run the below command to create a personalized `docker-compose.yml` you will use for creating the docker containers
Provide your lastname for username and it will choose a random, currently-free host port and embed your username in container/network names.

```bash
python3 generate_setup_files.py --username 
```

When the script finishes it will print the selected host port and the randomized container port, for example:

Host port: 23456
Container port: 52345

Use those values when capturing or connecting from the host. The compose file maps the printed host port to the printed container port. 

Note:  Use `--overwrite` if you need to regenerate and replace an existing `docker-compose.yml`.



What the generator creates
-------------------------
- A `docker-compose.yml` in the repository root. The generated compose maps a random high-number host port to a randomized container-side port (the script picks a container port unique per run/user). The generator prints both the host port and the container port.
- The compose uses two services `server` and `client` with container names like `csci-server-<name>` and `csci-client-<name>` and a dedicated bridge network `csci-net-<name>`.
- Creates Folders `server-<name>` and `client-<name>` that are shared with the server and client containers.
- The generated `docker-compose.yml` mounts local directories into the containers with a `volumes` entry, for example:

	- ./server-<name>:/app

Because of this bind mount, any files you create or edit inside `/app` in the container (for example `server.py`) are stored on the host in `server-<name>/`. That makes your implementation persistent across container restarts or recreations. 


Complete Client/Server Code (**3 Points**)
------------------------------------
- You can find a template of `server.py` and `client.py` file under the templates folder. Complete the missing steps in the file and copy them to their respective shred directory `server.py` --> `server-<name>` folder and `client.py` --> `client-<name>` folder. Any changes made to these files inside these folders would also be reflected within the containers.

- server.py
	- Listen on server container port.
	- Accept TCP connections and echo back any data received (simple echo service).

- client.py
	- Connect to host `SERVER_HOST` and port `SERVER_PORT` 
	- Send a short text message, receive the echo, print it, then exit.


Docker Commands Start/stop and run (**2 Points**)
-----------------------------------
After running `generate_setup_files.py` and creating `server-<name>/server.py` and `client-<name>/client.py`, start the setup:

```bash
# Start in the background
docker compose up -d

```

Useful Docker commands
----------------------
Quick commands to inspect containers, networks, and control the stack.

```bash
# List running containers (host-level)
docker ps

# List all containers (including stopped)
docker ps -a

# Show containers started by compose (preferred)
docker compose ps

# List Docker networks
docker network ls

# Inspect a specific network (replace <network-name>)
docker network inspect <network-name>

# Stop containers started by compose (keeps them around)
docker compose stop

# Stop and remove containers, networks, and default volumes
docker compose down
```

Run the following commands to start the server program 

```bash
# Open a shell in the server container
docker compose exec server bash

# inside the container
python server-jesse.py
```

Run the following commands to start the client program 

```bash
# Open a shell in the client container
docker compose exec client bash

# inside the container
python client-jesse.py
```

Network Sniffing (**2 Points**)
-------------------------------

Use a network sniffer such as Wireshark or tcpdump to capture at least 5 messages exchanged between the client and server containers. Make sure to select the appropriate network interface for capturing the traffic. Determine which interface to use by inspecting your Docker network setup.

- Filter traffic based on protocol tcp and port
- Look for the TCP three-way handshake (SYN, SYN/ACK, ACK), the data segment(s) containing your payload in plain text, and the FIN/ACK sequence when the connection closes
- Take screenshots that show: the TCP handshake, an example data exchange (client->server and server->client)


Deliverable - Part I (submit to eLC)
-------------------------
Include all of the following in a single PDF (the order below is suggested):

1. Add a paragraph explaining your understanding of the docker_compose file and its output. 
2. Updated `server.py` and `client.py` source files. Add inline comments in your code to explain the changes you made.
3. Mention any challenges faced in making the client and server(C/S) communicate and how you resolved it. 
4. Describe in detail steps you followed to sniff the C/S traffic and include multiple screenshots.
5. List the following observations : Client IP, Server IP, TCP Seq and ACK numbers.


Part II — Proxy or Multi‑client Server (choose one) ( 2 Points)
--------------------------------------------------

Choose one of the two options below and update the docker setup produced by the generator accordingly. Be brief and make implementations testable with the generated compose stack.

**Option A — Proxy as a separate container**
- Docker changes:
	- Implement proxy.py in a new proxy-<name>/ folder created alongside server-<name>/ and client-<name>/.  
		- Listen on PROXY_PORT (env var or constant).  
		- For each incoming client connection, connect to server through the proxy and forward bytes bidirectionally (simple relay). Log client addr, bytes forwarded, connect/disconnect, and close cleanly on EOF/errors.
	- Update the docker compose file as needed.

- Tests required:
	-  Capture screenshots of Proxied session: capture traffic showing client→proxy→server→proxy→client, and show proxy logs reporting bytes forwarded.
	
***Option B — Extend server to accept multiple clients**
- Modify server.py to accept and service concurrent clients. Log per-client events and bytes forwarded/echoed.
- Docker changes:
	- Ensure docker-compose.yml allows running multiple client containers so you can test concurrency against the single server container.
- Tests required:
	- Show server logs handling multiple simultaneous client connections.
	- Capture screenshots of netowrk traffic demonstrating distinct TCP flows from each client to the server.

Deliverable - Part II (submit to eLC)
-------------------------
- Modified/added code: proxy.py (if Option A), updated server.py and/or client.py.
- Updated docker-compose.yml.
- Short README paragraph explaining PROXY_PORT, SERVER_PORT, SERVER_HOST, how to start the proxy/server, and how to scale/run multiple clients.
- Screenshots to demonstrate the tests for the selected option.

