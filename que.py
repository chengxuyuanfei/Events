from Queue import Queue

def get(q):
    print "get", q.get()
    print "q", q

q = Queue()
q.put("first")
q.put("second")
print q
get(q)
print q
