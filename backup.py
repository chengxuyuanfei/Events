from enum import Enum

class PollerMask(Enum):
    POLLERREAD = 0
    POLLERWRITE = 1
    POLLERERROR = 2



class Poller(object):
    def __init__(self):
        try:
            raise ImportError
            from select import epoll
            self.poller_type = PollerType.EPOLL
            self.poller = epoll()
        except ImportError as e:
            # logging
            from select import select
            self.poller_type = PollerType.SELECT
            self.poller = None
            self.fds = set([])



    def register(self, fd, mask):
        import select       # for eventmask
        if self.poller_type is PollerType.EPOLL:        # raise type exception
            self.poller.register(fd, mask)
        elif self.poller_type is PollerType.SELECT:
            self.fds.add((fd, mask))

    def modify(self, fd, mask):
        if self.poller_type is PollerType.EPOLL:
            self.poller.modify(fd, mask)
        elif self.poller_type is PollerType.SELECT:
            self.fds.add((fd, mask))

    def unregister(self):
        pass

    def poll(self, timeout):
        if self.poller_type is PollerType.EPOLL:
            events = self.poller.poll(timeout)
            results = set({})
            import select       # for eventmask
            for fd, mask in events:
                if mask & select.EPOLLIN:
                    results.add((fd, PollerMask.POLLERREAD))
                elif mask & select.EPOLLOUT:
                    results.add((fd, PollerMask.POLLERWRITE))
                elif mask & select.EPOLLHUP:
                    results.add((fd, PollerMask.POLLERERROR))
            return results
        elif self.poller_type is PollerType.SELECT:
            inputs = []
            outputs = []
            for elem in self.fds:
                if elem[1] is PollerMask.POLLERREAD:
                    inputs.append(elem[0])
                elif elem[1] is PollerMask.POLLERWRITE:
                    outputs.append(elem[0])
                elif elem[1] is PollerMask.POLLERERROR:
                    pass
            from select import select
            reads, writes, errors = select(inputs, outputs, inputs, timeout)
            results = set([])
            for read in reads:
                results.add((read, PollerMask.POLLERREAD))
            for write in writes:
                results.add((write, PollerMask.POLLERWRITE))
            for error in errors:
                results.add((error, PollerMask.POLLERERROR))
            return results


