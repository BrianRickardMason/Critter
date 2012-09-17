import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")

i = 0
while True:
    request = "Content: %s." % i
    socket.send(request)
    print "Request: '%s'." % request
    response = socket.recv()
    print "Response: '%s'." % response
    i+=1
    time.sleep(1)
