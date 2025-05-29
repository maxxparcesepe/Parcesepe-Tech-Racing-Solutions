import socket
import struct
import csv
import os
from datetime import datetime

# === CSV Setup ===
filename = "C:/Users/awsom/Documents/SimRacingLogger/telemetry_log.csv"
file_exists = os.path.exists(filename)
csv_file = open(filename, mode='a', newline='')
csv_writer = csv.writer(csv_file)

terminal_log = open("terminal_log.txt", mode="a", encoding="utf-8")
# Log terminal output to file


headers = [
    "Timestamp",
    "Susp_FL", "Susp_FR", "Susp_RL", "Susp_RR",
    "Wheel_FL", "Wheel_FR", "Wheel_RL", "Wheel_RR",
    "Throttle", "Brake", "Speed", "Gear", "RPM",
    "G_Force_X", "G_Force_Y", "PacketSize"
]

if not file_exists:
    csv_writer.writerow(headers)

# === UDP Setup ===
UDP_IP = "127.0.0.1"
UDP_PORT = 20777
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(1.0)

print(f"Listening on {UDP_IP}:{UDP_PORT} for telemetry packets...")

try:
    while True:
        try:
            data, addr = sock.recvfrom(2048)
            packet_size = len(data)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

            # Default values
            susp = [0.0] * 4
            wheels = [0.0] * 4
            throttle = brake = speed = rpm = g_force_x = g_force_y = 0.0
            gear = -1

            if packet_size >= 148:
                susp = struct.unpack_from('<ffff', data, 32)
                wheels = struct.unpack_from('<ffff', data, 112)

            if packet_size >= 572:
                throttle = struct.unpack_from('<f', data, 540)[0]
                brake = struct.unpack_from('<f', data, 544)[0]
                speed = struct.unpack_from('<f', data, 548)[0]
                gear = struct.unpack_from('<b', data, 550)[0]
                rpm = struct.unpack_from('<f', data, 556)[0]
                g_force_x = struct.unpack_from('<f', data, 564)[0]
                g_force_y = struct.unpack_from('<f', data, 568)[0]

            # Log
            csv_writer.writerow([
                timestamp,
                *susp,
                *wheels,
                throttle,
                brake,
                speed,
                gear,
                rpm,
                g_force_x,
                g_force_y,
                packet_size
            ])
            csv_file.flush()

            log_message = f"[{timestamp}] Logged packet ({packet_size} bytes)"
            print(log_message)
            terminal_log.write(log_message + "\n")
            terminal_log.flush()

        except socket.timeout:
            continue
except KeyboardInterrupt:
    print("\nStopped by user.")
    csv_file.close()
    sock.close()
    terminal_log.close()
    print(f"Log saved to {filename}")
