import socket
import sys
import time
import json

HOST = "127.0.0.1"
BUFSIZE = 4096
START_SIZE = 2
INCR = "add100"
FILEPATH = "/app/z36_dgram_times"
REPEATS = 10

actions = {
    "inc": lambda x: x + 1,
    "add100": lambda x: x + 100,
    "add1000": lambda x: x + 1000,
    "mul": lambda x: x * 2,
}


def save_times(filename, times, sizes, params):
    with open(filename, "w") as f:
        json.dump({"sizes": sizes, "times": times, "params": params}, f)
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

    start_size = START_SIZE
    incr_action = actions[INCR]

    times = []
    dgram_sizes = []

    print("Starting experiment")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        size = start_size
        while True:
            try:
                single_size_times = []
                for _ in range(REPEATS):
                    message = b"x" * size
                    start = time.perf_counter()

                    s.sendto(message, (host, port))
                    data = s.recv(BUFSIZE)

                    duration = time.perf_counter() - start
                    single_size_times.append(duration)

                avg_time = sum(single_size_times) / REPEATS
                print(f"For datagram size of {size}B average time: {avg_time}s")

                times.append(avg_time)
                dgram_sizes.append(size)
                size = incr_action(size)

            except Exception as e:
                print(f"Failed for {size}B")
                print(e)
                break
    print("Client finished.")

    # Parametry do wykresu
    params = {
        "host": host,
        "port": port,
        "start_size": start_size,
        "incr_action": INCR,
        "repeats": REPEATS,
    }
    filename = f"{FILEPATH}_{INCR}_{REPEATS}.json"
    save_times(filename, times, dgram_sizes, params)
