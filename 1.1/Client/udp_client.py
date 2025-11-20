import socket
import sys
import time
import json

HOST = "127.0.0.1"
BUFSIZE = 4096
START_SIZE = 2
INCR = "mul"

actions = {
    "inc": lambda x: x + 1,
    "add100": lambda x: x + 100,
    "add1000": lambda x: x + 1000,
    "mul": lambda x: x * 2,
}


def save_times(filename, times, sizes):
    with open(filename, "w") as f:
        json.dump({"sizes": sizes, "times": times}, f)
    print("Times saved")


if __name__ == "__main__":
    print("This is UDP client.")

    if len(sys.argv) < 3:
        print("no port and/or host, using localhost:8000")
        port = 8000
        host = HOST
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])

    # Parametry dla wygdniejszego uruchamiania do pomiarów
    if len(sys.argv) == 4:
        start_size = int(sys.argv[3])
        incr_action = sys.argv[4]
    else:
        start_size = START_SIZE
        incr_action = actions[INCR]

    times = []
    dgram_sizes = []

    print("Starting experiment")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        size = start_size
        while True:
            try:
                message = b"x" * size
                start = time.perf_counter()
                s.sendto(message, (host, port))
                data = s.recv(BUFSIZE)
                duration = time.perf_counter() - start
                print(f"For datagram size of {size}B it took {duration}s to get answer")

                times.append(duration)
                dgram_sizes.append(size)
                size = incr_action(size)

            except Exception as e:
                print(f"Failed for {size}B")
                print(e)
                break
    print("Client finished.")

    save_times(
        f"/app/z36_dgram_times_{start_size}_{incr_action}.json", times, dgram_sizes
    )
