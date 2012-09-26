import threading

class MessageRouter(threading.Thread):
    def __init__(self, aPostOffice):
        self.mPostOffice = aPostOffice

        threading.Thread.__init__(self, name='MessageRouter')

    def run(self):
        while True:
            message = self.mPostOffice.getIncomingAnnouncement()

            # Forward the message to the rites.
            for key in self.mPostOffice.mCritter.mRites.iterkeys():
                self.mPostOffice.putMessage(key, message)
