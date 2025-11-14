import socket
import sys
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
times = {}
sizes = [2, 4, 8, 16, 32]

# TODO Implement better way of finding what is the maximum size of datagram

if  len(sys.argv) < 3: 
    print("no port and/or host, using localhost:5005")
    port=5005
    host=HOST
else:
    host = sys.argv[1]
    port = int( sys.argv[2] )

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for size in sizes:
    try:
        message = bytes()
        start = time.process_time()
        data = sock.sendto(message, (host, port))
        finish = time.process_time()
        times[size] = (finish - start)
    except Exception:
        break
