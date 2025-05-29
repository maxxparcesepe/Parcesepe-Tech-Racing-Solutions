import socket
from datetime import datetime
import os
import struct

# === Config ===
UDP_IP = "127.0.0.1"
UDP_PORT = 20778
LOG_FILE = "udp_raw_packets.log"

# === Create/append to the log file ===
log_path = os.path.join(os.getcwd(), LOG_FILE)
log_file = open(log_path, mode="a", encoding="utf-8")

print(f"📡 Listening for UDP packets on {UDP_IP}:{UDP_PORT}")
print(f"📝 Logging raw packets to: {log_path}")
print("🎮 Press Ctrl+C to stop.\n")

# === Setup socket ===
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(1.0)  # Non-blocking wait

try:
    while True:
        try:
            data, addr = sock.recvfrom(2048)  # Accept up to 2 KB packets
            packet_size = len(data)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

            hex_dump = data.hex()
            binary_dump = " ".join(format(byte, '08b') for byte in data)

            # Write to log file
            log_file.write(f"\n[{timestamp}] Packet from {addr} | Size: {packet_size} bytes\n")
            log_file.write(f"HEX: {hex_dump[:200]}...\n")  # Truncated for readability
            log_file.write(f"BIN: {binary_dump[:200]}...\n")

            # === New: Console Output for Analysis ===
            print(f"[{timestamp}] {packet_size} bytes received")
            print(f" → HEX (first 64): {hex_dump[:64]}...")

            try:
                float_values = struct.unpack_from('<16f', data, 0)  # Show first 16 floats
                float_preview = ", ".join(f"{v:.2f}" for v in float_values)
                print(f" → Float Preview: {float_preview}")
            except Exception as e:
                print(f" → Could not unpack floats: {e}")

        except socket.timeout:
            continue
except KeyboardInterrupt:
    print("\n🛑 Logging stopped by user.")
    log_file.close()
    sock.close()
    print(f"✅ Log saved to: {log_path}")

