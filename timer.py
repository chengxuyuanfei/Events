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
        self.times = set()    # set能够自动避免重复元素

    def __when_sec(self, sec):
        return int(time.time()) + sec

    def register(self, id, sec, mask):
        self.times.add((id, self.__when_sec(sec), mask, sec))

    def modify(self, event_id):
        pass

    def unregister(self):
        pass

    def latest_timespan(self):
        if self.latest_timespan_value is None:
            return 10
        return self.latest_timespan_value

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
                    self.times.add((id, self.__when_sec(sec), mask, sec))
                latest = 0
            else:
                if latest is None:
                    latest = when_sec
                if when_sec < latest:
                    latest = when_sec
        if latest is None:
            self.latest_timespan_value = None
        elif latest is 0:
            self.latest_timespan_value = 0
        else:
            self.latest_timespan_value = latest - time.time()
        return results
