import socket
from multiprocessing.dummy import Pool as ThreadPool
import threading
import json
def test(thread_id):
    for x in xrange(1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('192.168.72.132', 5354))
        import time
        request = dict()
        request["thread_id"] = thread_id
        request['times'] = x
        request['send_time'] = time.time()
        request['content'] = "This is a test example"
        # time_cur = time.time()
        sock.send(json.dumps(request))
        reply = sock.recv(1024)
        # print reply
        sock.close()
        # time.sleep(1)


import time
request = dict()
request["thread_id"] = 1
request['times'] = 2233
request['send_time'] = time.time()
request['content'] = "This is a test example"
# time_cur = time.time()
print len(json.dumps(request))
pool = ThreadPool(8)
args = [id for id in xrange(1000000)]
pool.map(test, args)

