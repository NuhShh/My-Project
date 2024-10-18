import socket
import sys
import time

server_address = ('192.168.0.14', 6969)
buffer_size = 1024

def handle_client(connection_socket, addr):
    """Handles a client connection, processing file requests."""
    print(f'Connection received from: {addr}')

    try:
        start_time = time.time()

        message = connection_socket.recv(buffer_size).decode()
        filename = message.split()[1]

        with open(filename[1:], 'rb') as f:
            file_data = f.read()

        response = f"HTTP/1.1 200 OK\r\n\r\n".encode()
        connection_socket.sendall(response)

        connection_socket.sendall(file_data)

        end_time = time.time()
        print(f"Request from {addr} processed in {end_time - start_time:.5f} seconds.")

    except IOError:
        error_response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        connection_socket.sendall(error_response)

        end_time = time.time()
        print(f"Request from {addr} failed: File not found. Processed in {end_time - start_time:.5f} seconds.")

    finally:
        connection_socket.close()

def main():
    """Sets up the server socket and listens for connections."""
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(server_address)
        server_socket.listen(1)
        print('The server is ready to receive')

        while True:
            connection_socket, addr = server_socket.accept()
            handle_client(connection_socket, addr)

    except KeyboardInterrupt:
        print("Server stopped by user.")

    finally:
        # Close server socket
        server_socket.close()
        sys.exit()

if __name__ == "__main__":
    main()
