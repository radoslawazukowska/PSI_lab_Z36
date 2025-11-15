import socket
import sys
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
times = {}
sizes = [2, 4, 8, 16, 32]

print("This is UDP client!!!")

# TODO Implement better way of finding what is the maximum size of datagram

if  len(sys.argv) < 3: 
    print("no port and/or host, using localhost:5005")
    port=8000
    host=HOST
else:
    host = sys.argv[1]
    port = int( sys.argv[2] )

print('Starting experiment')

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    for size in sizes:
        try:
            message = b"x" * size
            start = time.perf_counter()
            s.sendto(message, (host, port))
            data, addr = s.recvfrom(4096)
            finish = time.perf_counter()
            times[size] = (finish - start)
            print(f'For size of {size}B it took {time[size]}s to get answer')
        except Exception:
            print(f"Failed for {size}B")
            break

print('Client finished.')
