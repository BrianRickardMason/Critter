import sys
import threading
import zmq

from Critter.Critter import Critter

class CresponderWork(threading.Thread):
    def __init__(self):
        self.mContext = zmq.Context()

        self.mSocket = self.mContext.socket(zmq.REP)
        self.mSocket.bind('tcp://127.0.0.1:5555')

        threading.Thread.__init__(self, name='CresponderWork')

    def run(self):
        while True:
            request = self.mSocket.recv()
            print "Received request: '%s'" % request
            self.mSocket.send(request)

class Cresponder(Critter):
    def __init__(self, aCrittnick, aRites):
        Critter.__init__(self, aCrittnick , aCrittnick, aRites)

        self.mCresponderWork = CresponderWork()
        self.mCresponderWork.setDaemon(True)
        self.mCresponderWork.start()

if __name__ == "__main__":
    critter = Cresponder(sys.argv[1], [])
    critter.run()
