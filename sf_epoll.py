# -*- coding: utf-8 -*-
from Events import *
import socket

total = dict()


def request_response_process(event):
    if event.mask is PollerMask.POLLERREAD:
        if event.fd is server_socket:
            if not total.has_key("start time"):
                total['start time'] = time.time()
            if not total.has_key("connections"):
                total['connections'] = 0
            total['connections'] = total["connections"] + 1
            client_sock, client_addr = server_socket.accept()
            client_sock.setblocking(0)
            event.events.add_file_event(client_sock, PollerMask.POLLERREAD)
# @profile
def request_response_read_proc(event):
    if event.fd is server_socket:
        client_sock, client_addr = server_socket.accept()
        client_sock.setblocking(0)
        client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)       # 取消Nagle算法，保证尽快交付，经过测试，能够提升并发数量
        # client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 0)        # 设置小包延迟发送，等待可以组装成大包后再发送，理论上能够提高网络传输效率，但是在本应用场景的实测中，没有提升效果，反而有降低并发数量的现象
        event.events.add_file_event(client_sock, PollerMask.POLLERREAD, request_response_read_proc)
        if not total.has_key("start time"):
            total['start time'] = time.time()
        if not total.has_key("connections"):
            total['connections'] = 0
        total['connections'] = total['connections'] + 1

    else:
        # try except
        try:
            data = event.fd.recv(1024)
            if data:
                # print data
                event.events.add_file_event(event.fd, PollerMask.POLLERWRITE, request_response_write_proc, data)
            # else: # 没必要，write完毕后socket已经被关闭
            #     event.events.remove_file_event(event.fd)
            #     event.fd.close()
        except Exception as e:
            print e.message



# @profile
def request_response_write_proc(event):
    if event.client_data is not None:
        event.fd.send(event.client_data)
    event.events.remove_file_event(event.fd)
    event.fd.close()
    if not total.has_key("end time"):
        total['end time'] = time.time()
    if not total.has_key("complete"):
        total['complete'] = 0
    total['end time'] = time.time()
    total['complete'] = total['complete'] + 1
    total['timespan'] = total['end time'] - total['start time']
    total['speed'] = total['complete'] / float(total['timespan'])
    # print total
# @profile
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
event_loop.add_file_event(server_socket, PollerMask.POLLERREAD, request_response_read_proc)
event_loop.add_time_event(3, TimerMask.TIMERPERIOD, time_process)
# for x in range(150):
#     event_loop.add_time_event(x, TimerMask.TIMERPERIOD, time_process)
event_loop.run()

