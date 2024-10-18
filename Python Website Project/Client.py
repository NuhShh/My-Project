import socket
import sys
import threading

def send_request(server_addr, path, num_requests=1):
    threads = []
    for _ in range(num_requests):
        thread = threading.Thread(target=make_request, args=(server_addr, path))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def make_request(server_addr, path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(server_addr)
        request = f"GET {path} HTTP/1.1\r\nHost: {server_addr[0]}\r\nConnection: close\r\n\r\n"
        s.sendall(request.encode())
        response = s.recv(1024).decode()
        print(response)

if __name__ == "__main__":
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print("Usage: python client.py <server_host> <server_port> <path> [<num_requests>]")
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    path = sys.argv[3]
    num_requests = 1 if len(sys.argv) == 4 else int(sys.argv[4])

    send_request((server_host, server_port), path, num_requests)
