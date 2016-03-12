class father(object):
    def print_father(self):
        print "father"

class son(father):
    def print_father(self, son_str = "son"):
        print son_str


tmp = son()
tmp.print_father()

l = list()
# print l.pop()
print 'test', l.append(1)
l.append(3)
l.append(5)
l.remove(5)
print len(l)
print l.pop(), l

print l.pop(), l
for x in xrange(2, 5):
    print x
import time
for x in xrange(10):
    print time.time(), int(time.time()), type(time.time()), time.time() > int(time.time())

d = dict()
d[1] = [1, 2, 3]
d[2] = [4, 5, 6]
print "*************", d
del d[2]
print d
d[1][2] = 2
print d
s = set()
s.add((1, 2, 3))
s.add((1, 2, 5))
s.add((7, 8, 9))
print s




import json
request = dict()
request["thread_id"] = 1
request['times'] = x
request['send_time'] = time.time()
request['content'] = "This is a test example"
print json.dumps(request)
