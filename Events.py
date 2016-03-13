# -*- coding: utf-8 -*-
from poller import *
from timer import *

class Events(object):
    def __init__(self):
        self.poller = Poller()
        self.timer = Timer()
        self.time_id_generator = IDGenerator()
        self.time_events = TimeEvents()
        self.fd_clientdata = {}
        self.r_proc = None
        self.w_proc = None

    def set_file_read_proc(self, read_proc):
        self.r_proc = read_proc

    def set_file_write_proc(self, write_proc):
        self.w_proc = write_proc

    def add_read_file_event(self, fd, client_data = None):
        self.poller.register(fd, PollerMask.POLLERREAD)
        self.fd_clientdata[(fd, PollerMask.POLLERREAD)] = client_data

    def add_write_file_event(self, fd, client_data = None):
        self.poller.register(fd, PollerMask.POLLERWRITE)
        self.fd_clientdata[(fd, PollerMask.POLLERWRITE)] = client_data

    def remove_read_file_event(self, fd):
        self.poller.unregister(fd)
        del self.fd_clientdata[(fd, PollerMask.POLLERREAD)]
        fd.close()

    def remove_write_file_event(self, fd):
        self.poller.unregister(fd)
        del self.fd_clientdata[(fd, PollerMask.POLLERWRITE)]
        fd.close()

    def remove_file_event(self, fd):
        if self.fd_clientdata.has_key((fd, PollerMask.POLLERREAD)):
            del self.fd_clientdata[(fd, PollerMask.POLLERREAD)]
        if self.fd_clientdata.has_key((fd, PollerMask.POLLERWRITE)):
            del self.fd_clientdata[(fd, PollerMask.POLLERWRITE)]
        self.poller.unregister(fd)
        fd.close()

    # @profile
    def run(self):
        # process time event
        while 1:
            time_events = self.timer.poll()
            # print "time events", time_events
            for id in time_events:
                self.time_events.get(id).time_proc(self.time_events.get(id))
            # print self.timer.latest_timespan_value, self.timer.latest_timespan()
            file_events = self.poller.poll(self.timer.latest_timespan())
            # print "file events", file_events, len(file_events)
            # file_events = self.poller.poll(0)
            if len(file_events) is not 0:
                for fd, mask in file_events:    # poll出的数据如果不立刻处理，会马上又被poll出来，并不会积累到一定数量再poll
                    if mask is PollerMask.POLLERREAD:
                        self.r_proc(fd, self.fd_clientdata[(fd, mask)])
                    elif mask is PollerMask.POLLERWRITE:
                        self.w_proc(fd, self.fd_clientdata[(fd, mask)])

    #
    # @profile
    # def add_file_event(self, fd, mask, file_proc, client_data = None):
    #     self.poller.register(fd, mask)
    #
    #     self.file_events.put(self, fd, mask, file_proc, client_data)

    # def remove_file_event(self, fd):
    #     self.poller.unregister(fd)


    def add_time_event(self, sec, mask, time_proc, client_data = None):
        event_id = self.time_id_generator.get()
        self.time_events.put(self, event_id, mask, sec, time_proc, client_data)
        self.timer.register(event_id, sec, mask)

    def __process_event(self):
        pass

    # @profile
    # def run(self):
    #     # process time event
    #     while 1:
    #         time_events = self.timer.poll()
    #         # print "time events", time_events
    #         for id in time_events:
    #             self.time_events.get(id).time_proc(self.time_events.get(id))
    #         # print self.timer.latest_timespan_value, self.timer.latest_timespan()
    #         file_events = self.poller.poll(self.timer.latest_timespan())
    #         # print "file events", file_events, len(file_events)
    #         # file_events = self.poller.poll(0)
    #         for fd, mask in file_events:    # poll出的数据如果不立刻处理，会马上又被poll出来，并不会积累到一定数量再poll
    #             self.file_events.get(fd, mask).proc(self.file_events.get(fd, mask))


# FileEvents独立为一个类，保证可扩展
class FileEvents(object):
    def __init__(self):
        self.events = dict()

    def put(self, events, fd, mask, file_proc, client_data = None):
        self.events[(fd, mask)] = FileEvent(events, fd, mask, file_proc, client_data)   # 必须添加events，否则无法添加fd来监听

    def clear(self):
        pass

    def get(self, fd, mask):
        return self.events[(fd, mask)]

class FileEvent(object):
    def __init__(self, events, fd, mask, proc, client_data):
        self.events = events
        self.fd = fd
        self.mask = mask
        self.proc = proc
        self.client_data = client_data

class TimeEvents(object):
    def __init__(self):
        self.events = dict()

    def put(self, events, event_id, mask, sec, time_proc, client_data):
        self.events[event_id] = TimeEvent(events, event_id, mask, sec, time_proc, client_data)

    def clear(self):
        pass

    def get(self, event_id):
        return self.events[event_id]

class TimeEvent(object):
    def __init__(self, events, event_id, mask, sec, time_proc, client_data):
        self.events = events
        self.event_id = event_id
        self.mask = mask
        self.sec = sec
        self.time_proc = time_proc
        self.client_data = client_data



class EventFactory(object):
    pass

class IDGenerator(object):
    def __init__(self, floor = 0, ceiling = 256):
        self.free = list()
        self.used = list()
        self.__generator_id(floor, ceiling)


    def __generator_id(self, floor, ceiling):
        for x in xrange(floor, ceiling + 1):
            self.free.append(x)

    def get(self):
        ID = self.free.pop()
        self.used.append(ID)
        return ID

    def remove(self, ID):
        self.used.remove(ID)
        self.free.append(ID)
