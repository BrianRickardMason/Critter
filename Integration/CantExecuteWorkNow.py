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
        self.mRunsOn = Component_Worker_Worker1_Heartbeat

    def __call__(self, aComponent):
        if isinstance(aComponent, self.mRunsOn):
            worker1 = PiewikCritterData()
            worker1.assign({
                'type': Charstring().assign("Worker"),
                'nick': Charstring().assign("Worker1")
            })

            # TODO: Remove hardcoded value.
            for i in range(5):
                heartbeatAnnouncement = PiewikHeartbeatAnnouncement()
                heartbeatAnnouncement.assign({'messageName': Charstring().assign("HeartbeatAnnouncement"),
                                              'sender':      worker1,
                                              'timestamp':   Float().assign(time.time())})
                aComponent.mPort.send(heartbeatAnnouncement)
                # TODO: Remove hardcoded value.
                time.sleep(1)
        else:
            # TODO: Raise a meaningful exception.
            raise

class Function_RegisterResponse(Function):
    def __init__(self):
        self.mRunsOn = Component_Worker_Worker1_RegisterResponse

    def __call__(self, aComponent):
        if isinstance(aComponent, self.mRunsOn):
            balancer1 = PiewikCritterData()
            balancer1.assign({
                'type': Charstring().assign("Balancer"),
                'nick': Charstring().assign("Balancer1")
            })

            worker1 = PiewikCritterData()
            worker1.assign({
                'type': Charstring().assign("Worker"),
                'nick': Charstring().assign("Worker1")
            })

            presentYourselfRequest = PiewikPresentYourselfRequest()
            presentYourselfRequest.assign({
                'messageName': Charstring().assign("PresentYourselfRequest"),
                'sender':      balancer1,
                'receiver':    worker1
            })

            presentYourselfResponse = PiewikPresentYourselfResponse()
            presentYourselfResponse.assign({
                'messageName': Charstring().assign("PresentYourselfResponse"),
                'sender':      worker1,
                'receiver':    balancer1})

            aComponent.executeBlockingAction(
                Blocking(PortReceiveExpectation(aComponent.mPort, presentYourselfRequest)),
            )

            aComponent.mPort.send(presentYourselfResponse)
        else:
            # TODO: Raise a meaningful exception.
            raise

class Function_CommandWorkExecutionAnnouncement(Function):
    def __init__(self):
        self.mRunsOn = Component_GraphYeeti_GraphYeeti1

    def __call__(self, aComponent):
        if isinstance(aComponent, self.mRunsOn):
            # TODO: Should wait until the components know each other. Remove this hardcoded value.
            time.sleep(1)

            graphYeeti1 = PiewikCritterData()
            graphYeeti1.assign({'type': Charstring().assign("GraphYeeti"),
                                'nick': Charstring().assign("GraphYeeti1")})

            commandWorkExecutionAnnouncement = PiewikCommandWorkExecutionAnnouncement()
            commandWorkExecutionAnnouncement.assign({
                'messageName': Charstring().assign("CommandWorkExecutionAnnouncement"),
                'sender':      graphYeeti1,
                'graphName':   Charstring().assign("GraphName"),
                'cycle':       Integer().assign(1),
                'workName':    Charstring().assign("WorkName")
            })

            aComponent.mPort.send(commandWorkExecutionAnnouncement)
        else:
            # TODO: Raise a meaningful exception.
            raise

class Function_CantExecuteWorkNow(Function):
    def __init__(self):
        self.mRunsOn = Component_Worker_Worker1

    def __call__(self, aComponent):
        if isinstance(aComponent, self.mRunsOn):
            # TODO: Should wait until the components know each other. Remove this hardcoded value.
            time.sleep(1)

            worker1 = PiewikCritterData()
            worker1.assign({'type': Charstring().assign("Worker"),
                            'nick': Charstring().assign("Worker1")})

            balancer1 = PiewikCritterData()
            balancer1.assign({'type': Charstring().assign("Balancer"),
                              'nick': Charstring().assign("Balancer1")})

            executeWorkAnnouncement = PiewikExecuteWorkAnnouncement()
            executeWorkAnnouncement.assign({
                'messageName': Charstring().assign("ExecuteWorkAnnouncement"),
                'sender':      balancer1,
                'receiver':    worker1,
                'graphName':   Charstring().assign("GraphName"),
                'cycle':       Integer().assign(1),
                'workName':    Charstring().assign("WorkName")
            })

            cantExecuteWorkNowAnnouncement = PiewikCantExecuteWorkNowAnnouncement()
            cantExecuteWorkNowAnnouncement.assign({
                'messageName': Charstring().assign("CantExecuteWorkNowAnnouncement"),
                'sender':      worker1,
                'receiver':    balancer1,
                'graphName':   Charstring().assign("GraphName"),
                'cycle':       Integer().assign(1),
                'workName':    Charstring().assign("WorkName")
            })

            aComponent.executeBlockingAction(
                Blocking(PortReceiveExpectation(aComponent.mPort, executeWorkAnnouncement)),
            )

            aComponent.mPort.send(cantExecuteWorkNowAnnouncement)
        else:
            # TODO: Raise a meaningful exception.
            raise

class Mtc(Component):
    def __init__(self, aName, aTestcase):
        Component.__init__(self, aName)
        self.mTestcase = aTestcase

    def run(self):
        self.mTestcase.executePTC()

class Component_GraphYeeti_GraphYeeti1(Component):
    def __init__(self, aName):
        Component.__init__(self, aName)
        self.mPort = PiewikPort(self.mEventQueue)

class Component_Worker_Worker1(Component):
    def __init__(self, aName):
        Component.__init__(self, aName)
        self.mPort = PiewikPort(self.mEventQueue)

class Component_Worker_Worker1_Heartbeat(Component):
    def __init__(self, aName):
        Component.__init__(self, aName)
        self.mPort = PiewikPort(self.mEventQueue)

class Component_Worker_Worker1_RegisterResponse(Component):
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
        componentWorker1_Heartbeat = Component_Worker_Worker1_Heartbeat("Worker1_Heartbeat")
        componentWorker1_RegisterResponse = Component_Worker_Worker1_RegisterResponse("Worker1_RegisterResponse")
        componentGraphYeeti = Component_GraphYeeti_GraphYeeti1("GraphYeeti")
        componentWorker = Component_Worker_Worker1("Worker")

        componentGraphYeeti.setContext(self.mMtc, self)
        componentWorker.setContext(self.mMtc, self)
        componentWorker1_Heartbeat.setContext(self.mMtc, self)
        componentWorker1_RegisterResponse.setContext(self.mMtc, self)

        componentGraphYeeti.addFunction(Function_CommandWorkExecutionAnnouncement())
        componentWorker.addFunction(Function_CantExecuteWorkNow())
        componentWorker1_RegisterResponse.addFunction(Function_RegisterResponse())
        componentWorker1_Heartbeat.addFunction(Function_SendHeartbeat())

        componentGraphYeeti.start()
        componentWorker.start()
        componentWorker1_Heartbeat.start()
        componentWorker1_RegisterResponse.start()

        self.mMtc.executeBlockingAction(
            Interleave([
                Blocking(ComponentDoneExpectation(componentGraphYeeti)),
                Blocking(ComponentDoneExpectation(componentWorker)),
                Blocking(ComponentDoneExpectation(componentWorker1_RegisterResponse)),
                Blocking(ComponentDoneExpectation(componentWorker1_Heartbeat))
            ])
        )

testcase = SimpleTestcase()
control = Control()
control.execute(testcase)
