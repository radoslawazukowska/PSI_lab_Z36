import socket
import sys


if len(sys.argv) < 3:
    print("No port and/or host, using localhost:8888")
    PORT = 8888
    HOST = "127.0.0.1"
else:
    HOST = sys.argv[1]
    try:
        PORT = int(sys.argv[2])
    except ValueError:
        print("Invalid port number")
        sys.exit(1)

if len(sys.argv) < 4:
    MESSAGE = "hello world"
else:
    MESSAGE = sys.argv[3]

print(f"Sending message '{MESSAGE}' to {HOST}:{PORT}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(MESSAGE.encode())

    s.shutdown(socket.SHUT_WR)

    data = s.recv(1024)

print("Received:", data.decode())
print("Client finished.")
