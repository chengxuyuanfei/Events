import socket


while 1:
    request_str = raw_input("input:")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 5354))
    sock.send(request_str)
    reply = sock.recv(1024)
    print "reply:", reply, "length:", len(reply)
    sock.close()




