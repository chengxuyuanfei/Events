# -*- coding: utf-8 -*-
from poller import *
from timer import *


class Events(object):
    def __init__(self):
        self.poller = Poller()      # 文件事件处理器
        self.timer = Timer()        # 时间事件处理器
        self.file_events = FileEvents()     # 通过dict保存每个文件事件的各种信息，便于文件事件执行时获取各种信息
        self.time_events = TimeEvents()     # 通过dict保存每个文件事件的各种信息，便于文件事件执行时获取各种信息
        self.time_id_generator = IDGenerator()  # ID生成器，该ID用于标示时间时间，一个ID对应当前的一个时间事件

    # @profile
    def add_file_event(self, fd, mask, file_proc, client_data = None):
        self.poller.register(fd, mask)
        self.file_events.put(self, fd, mask, file_proc, client_data)

    def remove_file_event(self, fd):
        self.poller.unregister(fd)


    def add_time_event(self, sec, mask, time_proc, client_data = None):
        event_id = self.time_id_generator.get()
        self.time_events.put(self, event_id, mask, sec, time_proc, client_data)
        self.timer.register(event_id, sec, mask)


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
            for fd, mask in file_events:    # poll出的数据如果不立刻处理，会马上又被poll出来，并不会积累到一定数量再poll
                self.file_events.get(fd, mask).proc(self.file_events.get(fd, mask))


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

# 作为dict的value，保存文件事件执行时需要的各种信息
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

# 作为dict的value，保存时间事件执行时需要的各种信息
class TimeEvent(object):
    def __init__(self, events, event_id, mask, sec, time_proc, client_data):
        self.events = events
        self.event_id = event_id
        self.mask = mask
        self.sec = sec
        self.time_proc = time_proc
        self.client_data = client_data


# ID生成器
# 1，生成器生成的ID始终在floor&ceiling之间，包括边界
# 2，循环使用ID
# 3，在时间事件中，数量并不多，故而默认仅有257个ID
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
