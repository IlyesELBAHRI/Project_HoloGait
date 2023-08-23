import socket
import sys
from time import sleep

## Setup socket ##
host = "127.0.0.1"
port = 50000
addr = (host, port)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)  # 1sec timeout


def vibrate(n_tactors, freq, n_cycles):
    base_command = "!ChangeTactorState, {}, 7, {}"

    cycle = 0
    while cycle < n_cycles:
        for i in range(n_tactors):
            command = base_command.format(str(i), str(((1 / freq) / 2) * 10**3))
            sock.sendto(command.encode(), addr)
            try:
                print(
                    f"receiving: {sock.recvfrom(1024)[0]}"
                )  # 1024 bytes for receiving buffer
            except socket.timeout:
                print("No response from server")

        cycle += 1
        delay = 1 / freq
        sleep(delay)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python vibrate.py <n_tactors> <freq> <n_cycles>")
        sys.exit(1)

    n_tactors = int(sys.argv[1])
    freq = int(sys.argv[2])
    n_cycles = int(sys.argv[3])

    vibrate(n_tactors, freq, n_cycles)
