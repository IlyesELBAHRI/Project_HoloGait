import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("127.0.0.1", 8080))

while True:
    data, addr = s.recvfrom(1024)

    try:
        if int(data.decode()) == 1:
            s.sendto("Hello World".encode(), (addr[0], 8081))
    except:
        pass

    print(data.decode())
