import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("172.18.2.224", 8081))
s.setblocking(False)
s.settimeout(0.1)

while True:
    msg = input("Enter a message: ")
    s.sendto(msg.encode(), ("172.18.2.224", 8080))

    try:
        print(s.recv(1024).decode())
    except:
        pass
