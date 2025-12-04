import socket
import hashlib
import struct

HOST = '0.0.0.0'
PORT = 8080
BUFSIZE = 66000
ACK_SIZE = 4


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        ip, port = s.getsockname()
        print("Will listen on ", ip, ":", port)

        received_data = bytearray()
        expected_seq_num = 0

        while True:
            try:
                message, address = s.recvfrom( BUFSIZE )
                print(f"Message from Client:{message}")
                print(f"Client IP Address:{address}")

                packet_data = message[ACK_SIZE:]
                seq_num = struct.unpack('!I', message[:ACK_SIZE])[0]

                print(f"Received seq={seq_num} from {address}, payload_len={len(packet_data)}")

                if seq_num == expected_seq_num:
                    s.sendto(struct.pack('!I', seq_num), address)

                    if len(packet_data) == 0:
                        print("EOF received")
                        break

                    received_data.extend(packet_data)
                    expected_seq_num += 1
                elif seq_num < expected_seq_num:
                    s.sendto(struct.pack('!I', seq_num), address)

            except Exception as e:
                print(f"Server's error: {e}")

        hash = hashlib.sha256(received_data).hexdigest()
        print("Server reading ended")
        print(f"Server's hash: {hash}")
