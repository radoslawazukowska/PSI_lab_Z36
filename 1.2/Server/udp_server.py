import socket
import sys


HOST = '127.0.0.1'
port = 8080
BUFSIZE = 66000


if __name__ == "__main__":
    print("Will listen on ", HOST, ":", port)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, port))
        i = 1
        while i<10:
            data_address = s.recvfrom( BUFSIZE )
            data = data_address[0]
            address = data_address[1]
            print(f"Message from Client:{data}")
            print(f"Client IP Address:{address}")
            if not data:
                print("Error in datagram?")
                break
            s.sendto(data, address)
            print(f"sending dgram #{i}")
            i += 1
