import socket, select
import time

# @profile
def test():
    total = dict()
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('0.0.0.0', 5355))
    serversocket.listen(5)
    serversocket.setblocking(0)

    epoll = select.epoll()
    epoll.register(serversocket.fileno(), select.EPOLLIN)

    try:
        connections = {}; requests = {}; responses = {}
        while True:
            if total.has_key('complete') and total['complete'] % 4000 is 0:
                print total
            events = epoll.poll(1)
            # print 'events count:', len(events)
            for fileno, event in events:
                if fileno == serversocket.fileno():
                    connection, address = serversocket.accept()
                    connection.setblocking(0)
                    epoll.register(connection.fileno(), select.EPOLLIN)
                    connections[connection.fileno()] = connection
                    requests[connection.fileno()] = None
                    responses[connection.fileno()] = None
                    if not total.has_key("start time"):
                        total['start time'] = time.time()
                    if not total.has_key("connections"):
                        total['connections'] = 0
                    total['connections'] = total['connections'] + 1
                elif event & select.EPOLLIN:
                    requests[fileno] = connections[fileno].recv(1024)
                    if requests[fileno]:
                        epoll.modify(fileno, select.EPOLLOUT)
                        # print requests[fileno]
                    else:
                        epoll.unregister(fileno)
                        connections[fileno].close()
                elif event & select.EPOLLOUT:
                    byteswritten = connections[fileno].send(requests[fileno])
                    epoll.unregister(fileno)
                    connections[fileno].close()
                    if not total.has_key("end time"):
                        total['end time'] = time.time()
                    if not total.has_key("complete"):
                        total['complete'] = 0
                    total['end time'] = time.time()
                    total['complete'] = total['complete'] + 1
                    total['timespan'] = total['end time'] - total['start time']
                    total['speed'] = total['complete'] / float(total['timespan'])
    finally:
        epoll.unregister(serversocket.fileno())
        epoll.close()
        serversocket.close()

test()