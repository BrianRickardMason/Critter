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

class Function_SendHeartbeat(Function):
    def __init__(self):
        self.mRunsOn = Component_HelloCritty_HelloCritty2_Heartbeat

    def __call__(self, aComponent):
        if isinstance(aComponent, self.mRunsOn):
            helloCritty2 = PiewikCritterData()
            helloCritty2.assign({'type': Charstring().assign("HelloCritty"),
                                 'nick': Charstring().assign("HelloCritty2")})

            # TODO: Remove hardcoded value.
            for i in range(2):
                heartbeatAnnouncement = PiewikHeartbeatAnnouncement()
                heartbeatAnnouncement.assign({'messageName': Charstring().assign("HeartbeatAnnouncement"),
                                              'sender':      helloCritty2,
                                              'timestamp':   Float().assign(time.time())})
                aComponent.mPort.send(heartbeatAnnouncement)
                # TODO: Remove hardcoded value.
                time.sleep(1)
        else:
            # TODO: Raise a meaningful exception.
            raise

class Function_RegisterRequest(Function):
    def __init__(self):
        self.mRunsOn = Component_HelloCritty_HelloCritty2_RegisterRequest

    def __call__(self, aComponent):
        if isinstance(aComponent, self.mRunsOn):
            helloCritty1 = PiewikCritterData()
            helloCritty1.assign({'type': Charstring().assign("HelloCritty"),
                                 'nick': Charstring().assign("HelloCritty1")})

            helloCritty2 = PiewikCritterData()
            helloCritty2.assign({'type': Charstring().assign("HelloCritty"),
                                 'nick': Charstring().assign("HelloCritty2")})

            heartbeatAnnouncement = PiewikHeartbeatAnnouncement()
            heartbeatAnnouncement.assign({'messageName': Charstring().assign("HeartbeatAnnouncement"),
                                          'sender':      helloCritty2,
                                          'timestamp':   AnySingleElement()})

            presentYourselfRequest = PiewikPresentYourselfRequest()
            presentYourselfRequest.assign({'messageName': Charstring().assign("PresentYourselfRequest"),
                                           'sender':      helloCritty2,
                                           'receiver':    helloCritty1})

            presentYourselfResponse = PiewikPresentYourselfResponse()
            presentYourselfResponse.assign({'messageName': Charstring().assign("PresentYourselfResponse"),
                                            'sender':      helloCritty1,
                                            'receiver':    helloCritty2})

            aComponent.executeBlockingAction(
                Blocking(PortReceiveExpectation(aComponent.mPort, heartbeatAnnouncement)),
            )

            aComponent.mPort.send(presentYourselfRequest)

            aComponent.executeBlockingAction(
                Blocking(PortReceiveExpectation(aComponent.mPort, presentYourselfResponse)),
            )

        else:
            # TODO: Raise a meaningful exception.
            raise

class Function_RegisterResponse(Function):
    def __init__(self):
        self.mRunsOn = Component_HelloCritty_HelloCritty2_RegisterResponse

    def __call__(self, aComponent):
        if isinstance(aComponent, self.mRunsOn):
            helloCritty1 = PiewikCritterData()
            helloCritty1.assign({'type': Charstring().assign("HelloCritty"),
                                 'nick': Charstring().assign("HelloCritty1")})

            helloCritty2 = PiewikCritterData()
            helloCritty2.assign({'type': Charstring().assign("HelloCritty"),
                                 'nick': Charstring().assign("HelloCritty2")})

            presentYourselfRequest = PiewikPresentYourselfRequest()
            presentYourselfRequest.assign({'messageName': Charstring().assign("PresentYourselfRequest"),
                                           'sender':      helloCritty1,
                                           'receiver':    helloCritty2})

            presentYourselfResponse = PiewikPresentYourselfResponse()
            presentYourselfResponse.assign({'messageName': Charstring().assign("PresentYourselfResponse"),
                                            'sender':      helloCritty2,
                                            'receiver':    helloCritty1})

            aComponent.executeBlockingAction(
                Blocking(PortReceiveExpectation(aComponent.mPort, presentYourselfRequest)),
            )

            aComponent.mPort.send(presentYourselfResponse)
        else:
            # TODO: Raise a meaningful exception.
            raise

class Mtc(Component):
    def __init__(self, aName, aTestcase):
        Component.__init__(self, aName)
        self.mTestcase = aTestcase

    def run(self):
        self.mTestcase.executePTC()

class Component_HelloCritty_HelloCritty2_Heartbeat(Component):
    def __init__(self, aName):
        Component.__init__(self, aName)
        self.mPort = PiewikPort(self.mEventQueue)


class Component_HelloCritty_HelloCritty2_RegisterRequest(Component):
    def __init__(self, aName):
        Component.__init__(self, aName)
        self.mPort = PiewikPort(self.mEventQueue)

class Component_HelloCritty_HelloCritty2_RegisterResponse(Component):
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
        componentHeartbeat = Component_HelloCritty_HelloCritty2_Heartbeat("ComponentA1")
        componentRegisterRequest = Component_HelloCritty_HelloCritty2_RegisterRequest("ComponentA2")
        componentRegisterResponse = Component_HelloCritty_HelloCritty2_RegisterResponse("ComponentA2")

        componentHeartbeat.setContext(self.mMtc, self)
        componentRegisterRequest.setContext(self.mMtc, self)
        componentRegisterResponse.setContext(self.mMtc, self)

        componentHeartbeat.addFunction(Function_SendHeartbeat())
        componentRegisterRequest.addFunction(Function_RegisterRequest())
        componentRegisterResponse.addFunction(Function_RegisterResponse())

        componentHeartbeat.start()
        componentRegisterRequest.start()
        componentRegisterResponse.start()

        self.mMtc.executeBlockingAction(
            Interleave([
                Blocking(ComponentDoneExpectation(componentHeartbeat)),
                Blocking(ComponentDoneExpectation(componentRegisterRequest)),
                Blocking(ComponentDoneExpectation(componentRegisterResponse))
            ])
        )

testcase = SimpleTestcase()
control = Control()
control.execute(testcase)
