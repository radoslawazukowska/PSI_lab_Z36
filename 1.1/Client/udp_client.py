import socket
import sys
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
BUFSIZE = 4096
START_SIZE = 2

actions = {
    "increment": lambda x: x + 1,
    "add100": lambda x: x + 100,
    "add1000": lambda x: x + 1000,
    "mul": lambda x: x * 2,
}
action = "mul"

times = []
dgram_sizes = []

print("This is UDP client.")

if len(sys.argv) < 3:
    print("no port and/or host, using localhost:5005")
    port = 8000
    host = HOST
else:
    host = sys.argv[1]
    port = int(sys.argv[2])

print("Starting experiment")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    size = START_SIZE
    while True:
        try:
            message = b"x" * size
            start = time.perf_counter()
            s.sendto(message, (host, port))
            data = s.recv(BUFSIZE)

            finish = time.perf_counter()
            duration = finish - start

            print(f"For datagram size of {size}B it took {duration}s to get answer")

            times.append(duration)
            dgram_sizes.append(size)
            size = actions[action](size)
        except Exception as e:
            print(f"Failed for {size}B")
            print(e)
            break

print("Client finished.")
print(dgram_sizes)
print(times)
