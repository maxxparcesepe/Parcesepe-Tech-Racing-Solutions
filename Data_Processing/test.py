import socket
from datetime import datetime

UDP_IP = "127.0.0.1"
UDP_PORT = 20777

print(f"Listening on {UDP_IP}:{UDP_PORT}")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(1.0)

try:
    while True:
        try:
            data, addr = sock.recvfrom(2048)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

            print(f"Received {len(data)} bytes from {addr}")
            print(f"[{timestamp}] HEX DUMP (first 64 bytes): {data[:64].hex()}")

        except socket.timeout:
            continue
except KeyboardInterrupt:
    print("\nStopped by user.")
    sock.close()
