import socket
import threading
import time

server_address = ('192.168.0.14', 8000)
buffersize = 1024

def handle_client(conn, addr):
    try:
        start_time = time.time()

        request = conn.recv(buffersize).decode().split()
        filename = request[1]

        try:
            with open(filename[1:], 'rb') as f:
                content = f.read()

            conn.sendall("HTTP/1.1 200 OK\r\n\r\n".encode())

            conn.sendall(content)

        except FileNotFoundError:
            conn.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode())

        conn.close()

        print(f"Request from {addr} processed in {time.time() - start_time:.5f} seconds.")

    except Exception as e:
        print(f"Error handling request from {addr}: {e}")
        conn.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(5)
    print('The server is ready to receive')

    while True:
        conn, addr = server_socket.accept()
        print('Connection received from:', addr)
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

    server_socket.close()

if __name__ == "__main__":
    main()
