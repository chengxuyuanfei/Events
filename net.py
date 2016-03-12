from poller import *
import socket, select

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('0.0.0.0', 5354))
server_socket.listen(10)
server_socket.setblocking(0)

poller = Poller()
poller.register(server_socket.fileno(), PollerMask.POLLERREAD)
while 1:
    events = poller.poll(2)
    for fd, flag in events:
        print fd, flag
        if fd is server_socket.fileno():
            con, add = server_socket.accept()
            # con.setblocking(0)
            buf = con.recv(1024)
            con.close()
            print buf
    import time
    print time.time()