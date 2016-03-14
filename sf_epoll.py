# -*- coding: utf-8 -*-
from Events import *
import socket

total = dict()

def r_proc(fd, client_data):
    if fd is server_socket:
        client_sock, client_addr = server_socket.accept()
        client_sock.setblocking(0)
        client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        # client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 0)
        event_loop.add_read_file_event(client_sock, client_data)
        if not total.has_key("start time"):
            total['start time'] = time.time()
        if not total.has_key("connections"):
            total['connections'] = 0
        total['connections'] = total['connections'] + 1
    else:
        # try except
        try:
            data = fd.recv(1024)
            if data:
                # print data
                event_loop.add_write_file_event(fd, client_data)
            # else: # 没必要，write完毕后socket已经被关闭
            #     event.events.remove_file_event(event.fd)
            #     event.fd.close()
        except Exception as e:
            print e.message

def w_proc(fd, client_data):
    if client_data is not None:
        fd.send(client_data)
    event_loop.remove_file_event(fd)
    if not total.has_key("end time"):
        total['end time'] = time.time()
    if not total.has_key("complete"):
        total['complete'] = 0
    total['end time'] = time.time()
    total['complete'] = total['complete'] + 1
    total['timespan'] = total['end time'] - total['start time']
    total['speed'] = total['complete'] / float(total['timespan'])


def time_process(event):
    # print 'exec time process'
    # import time
    # print "time_process:", time.time()
    # x = time.time()
    print total

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('0.0.0.0', 5354))
server_socket.listen(5)
server_socket.setblocking(0)
event_loop = Events()
event_loop.set_file_read_proc(r_proc)
event_loop.set_file_write_proc(w_proc)
event_loop.add_read_file_event(server_socket)
event_loop.add_time_event(3, TimerMask.TIMERPERIOD, time_process)
# for x in range(150):
#     event_loop.add_time_event(x, TimerMask.TIMERPERIOD, time_process)
event_loop.run()

