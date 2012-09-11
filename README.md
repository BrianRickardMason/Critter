Critter
=======

Continuous Integration Redefined.


            for requestName in self.mSentReq:
#                print self.mSentReq[requestName].softTimeout
                for critthash in self.mSentReq[requestName]:
                    print self.mSentReq[requestName][critthash]['sentOn']
                    print time.time()
                    print self.mSentReq[requestName][critthash]['softTimeout']
                    print self.mSentReq[requestName][critthash]['hardTimeout']
