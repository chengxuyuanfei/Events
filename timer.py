# -*- coding: utf-8 -*-
import time

try:
    from enum import Enum
    class TimerMask(Enum):
        TIMERAPPOINTMENT = 0
        TIMERPERIOD = 1
except ImportError as e:
    class TimerMask():
        TIMERAPPOINTMENT = 0
        TIMERPERIOD = 1




class Timer(object):
    def __init__(self):
        self.times = set()    # set能够自动避免重复元素，且速度也很快，用于保存时间事件

    def __when_sec(self, sec):
        return int(time.time()) + sec

    def register(self, id, sec, mask):
        self.times.add((id, self.__when_sec(sec), mask, sec))

    def modify(self, event_id):
        pass

    def unregister(self):
        pass

    def latest_timespan(self):          # 最近即将到达的时间事件，距离事件执行的时间，用于文件事件poll中的sleep，，该值在每次poll后更新
        if self.latest_timespan_value is None:
            return 10
        return self.latest_timespan_value

    def __update_latest_timespan(self, latest):
        if latest is None:                          # 无时间事件注册
            self.latest_timespan_value = None       #
        elif latest is 0:                           # 有时间事件，且执行时间到达，需要立刻执行
            self.latest_timespan_value = 0
        else:                                       # 有时间事件，但是执行时间未到
            self.latest_timespan_value = latest - time.time()

    def poll(self):
        now = time.time()
        results = set()
        latest = None
        for id, when_sec, mask, sec in self.times:
            if when_sec <= now:
                results.add(id)
                if mask is TimerMask.TIMERAPPOINTMENT:
                    self.times.remove((id, when_sec, mask, sec))
                elif mask is TimerMask.TIMERPERIOD:
                    self.times.remove((id, when_sec, mask, sec))
                    self.times.add((id, self.__when_sec(sec), mask, sec))       # 周期性时间事件，当次poll出后，需要继续添加到times中，保证能够周期运行
                latest = 0
            else:
                if latest is None:
                    latest = when_sec
                if when_sec < latest:
                    latest = when_sec
        return results
