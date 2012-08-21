# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Piewik Project.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the project nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE PROJECT AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE PROJECT OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import time

from Piewik.Runtime.Action                                   import Alternative
from Piewik.Runtime.Action                                   import Blocking
from Piewik.Runtime.Action                                   import Interleave
from Piewik.Runtime.Component                                import Component
from Piewik.Runtime.Control                                  import Control
from Piewik.Runtime.Event                                    import PortReceivedEvent
from Piewik.Runtime.EventExpectation                         import ComponentDoneExpectation
from Piewik.Runtime.EventExpectation                         import PortReceiveExpectation
from Piewik.Runtime.Extensions.Critter.Interface.Translation import *
from Piewik.Runtime.Extensions.Critter.Port                  import PiewikPort
from Piewik.Runtime.Testcase                                 import Testcase

class Function(object):
    def __init__(self):
        self.mRunsOn = None

class Function_LoadWorkDetails(Function):
    def __init__(self):
        self.mRunsOn = Component_Worker_Worker1

    def __call__(self, aComponent):
        if isinstance(aComponent, self.mRunsOn):
            # TODO: Should wait until the components know each other. Remove this hardcoded value.
            time.sleep(1)

            cribrarian1 = PiewikCritterData()
            cribrarian1.assign({'type': Charstring().assign("Cribrarian"),
                                'nick': Charstring().assign("Cribrarian1")})

            worker1 = PiewikCritterData()
            worker1.assign({'type': Charstring().assign("Worker"),
                            'nick': Charstring().assign("Worker1")})

            loadWorkDetailsRequest = PiewikLoadWorkDetailsRequest()
            loadWorkDetailsRequest.assign({'messageName': Charstring().assign("LoadWorkDetailsRequest"),
                                           'sender':      worker1})

            # TODO: Should be verified in a more detailed way.
            loadWorkDetailsResponse = PiewikLoadWorkDetailsResponse()
            loadWorkDetailsResponse.assign({'messageName': Charstring().assign("LoadWorkDetailsResponse"),
                                            'sender':      cribrarian1,
                                            'receiver':    worker1,
                                            'details':     AnySingleElement()})

            aComponent.mPort.send(loadWorkDetailsRequest)

            aComponent.executeBlockingAction(
                Blocking(PortReceiveExpectation(aComponent.mPort, loadWorkDetailsResponse)),
            )
        else:
            # TODO: Raise a meaningful exception.
            raise

class Mtc(Component):
    def __init__(self, aName, aTestcase):
        Component.__init__(self, aName)
        self.mTestcase = aTestcase

    def run(self):
        self.mTestcase.executePTC()

class Component_Worker_Worker1(Component):
    def __init__(self, aName):
        Component.__init__(self, aName)
        self.mPort = PiewikPort(self.mEventQueue)

class SimpleTestcase(Testcase):
    def __init__(self):
        Testcase.__init__(self)
        self.mRunsOn = Mtc
        self.mMtc    = Mtc("MTC", self)

    def executeMTC(self):
        self.mMtc.start()
        self.mMtc.join()

    def executePTC(self):
        componentWorker = Component_Worker_Worker1("Worker")

        componentWorker.setContext(self.mMtc, self)

        componentWorker.addFunction(Function_LoadWorkDetails())

        componentWorker.start()

        self.mMtc.executeBlockingAction(
            Interleave([
                Blocking(ComponentDoneExpectation(componentWorker))
            ])
        )

testcase = SimpleTestcase()
control = Control()
control.execute(testcase)
