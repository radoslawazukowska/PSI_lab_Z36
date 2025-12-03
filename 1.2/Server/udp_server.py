import socket
import sys


HOST = '0.0.0.0'
PORT = 8080
BUFSIZE = 66000


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        ip, port = s.getsockname()
        print("Will listen on ", ip, ":", port)
        i = 1
        while i<10:
            print(f"Waiting for client's message #{i}")
            message, address = s.recvfrom( BUFSIZE )
            print(f"Message from Client:{message}")
            print(f"Client IP Address:{address}")
            if not message:
                print("Error in datagram?")
                break
            s.sendto(message, address)
            print(f"sending dgram #{i}")
            i += 1
