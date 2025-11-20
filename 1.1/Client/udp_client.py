import socket
import sys
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
BUFSIZE = 4096
# times = {}
# datagram_sizes = [60000, 65500, 65506, 65507, 65508]
times = []
dgram_sizes = []

print("This is UDP client.")

# TODO Implement better way of finding what is the maximum size of datagram

if len(sys.argv) < 3:
    print("no port and/or host, using localhost:5005")
    port = 8000
    host = HOST
else:
    host = sys.argv[1]
    port = int(sys.argv[2])

print("Starting experiment")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # s.bind(("0.0.0.0", 5000)) #UDP nie bindujemy
    # for size in datagram_sizes:
    size = 1
    while True:
        size *= 2
        dgram_sizes.append(size)
        try:
            message = b"x" * size
            start = time.perf_counter()
            s.sendto(message, (host, port))
            data = s.recv(BUFSIZE)
            # zamiana na recv zgodnie z prezentacją, odbiera tylko 26 bajtów
            finish = time.perf_counter()
            # times[size] = finish - start
            times.append(finish - start)
            print(f"For datagram size of {size}B it took {times[-1]}s to get answer")
        except Exception as e:
            print(f"Failed for {size}B")
            print(e)
            break

print("Client finished.")
print(dgram_sizes)
print(times)
