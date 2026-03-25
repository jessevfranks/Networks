import random
import socket
import sys
import time

def traceroute(destination):
    dest_ip = socket.gethostbyname(destination)

    max_ttl = 50
    timeout_seconds = 3

    for ttl in range(1, max_ttl+1):
        # Clean Linux raw socket
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        recv_socket.settimeout(timeout_seconds)

        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # Linux uses SOL_IP for standard socket options
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        dest_port = 33444
        src_port = 50000
        send_socket.bind(("", src_port))

        start_time = time.time()
        send_socket.sendto(b"", (dest_ip, dest_port))

        try:
            raw_data, addr = recv_socket.recvfrom(512)
            end_time = time.time()
            rtt = (end_time - start_time) * 1000 # Converted to milliseconds
            reply_ip = addr[0]

            # Prevent script crash if router has no hostname
            try:
                reply_hostname = socket.gethostbyaddr(reply_ip)[0]
            except socket.herror:
                reply_hostname = reply_ip

            print(f"{ttl:<2} {reply_hostname} ({reply_ip}) {rtt:.3f}ms")

            if reply_ip == dest_ip:
                break

        except socket.timeout:
            print(f"{ttl:<2} *")

        finally:
            recv_socket.close()
            send_socket.close()

if __name__ == "__main__":
    traceroute(sys.argv[1])