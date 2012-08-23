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

from Runtime.Action                                   import Alternative
from Runtime.Action                                   import Blocking
from Runtime.Action                                   import Interleave
from Runtime.Component                                import Component
from Runtime.Control                                  import Control
from Runtime.Event                                    import PortReceivedEvent
from Runtime.EventExpectation                         import ComponentDoneExpectation
from Runtime.EventExpectation                         import PortReceiveExpectation
from Runtime.Extensions.Critter.Interface.Translation import *
from Runtime.Extensions.Critter.Port                  import PiewikPort
from Runtime.Testcase                                 import Testcase

class TemplateBoolean(Boolean):
    def __init__(self):
        Boolean.__init__(self)
        self.mAcceptDecorator = TemplateAcceptDecorator(self.mAcceptDecorator, {})

class Function(object):
    def __init__(self):
        self.mRunsOn = None

class Function_SendExecuteWorkAnnouncement(Function):
    def __init__(self):
        self.mRunsOn = Component_Balancer_Balancer1

    def __call__(self, aComponent):
        if isinstance(aComponent, self.mRunsOn):
            # TODO: Should wait until the components know each other. Remove this hardcoded value.
            time.sleep(1)

            balancer1 = {
                'type': Charstring().assignValueType(CharstringValue("Balancer")),
                'nick': Charstring().assignValueType(CharstringValue("Balancer1"))
            }

            worker1 = {
                'type': Charstring().assignValueType(CharstringValue("Worker")),
                'nick': Charstring().assignValueType(CharstringValue("Worker1"))
            }

            executeWorkAnnouncement = PiewikExecuteWorkAnnouncement()
            executeWorkAnnouncement.assignValueType({
                'messageName': Charstring().assignValueType(CharstringValue("ExecuteWorkAnnouncement")),
                'sender':      balancer1,
                'receiver':    worker1,
                'graphName':   Charstring().assignValueType(CharstringValue("GraphName")),
                'cycle':       Integer().assignValueType(IntegerValue(22)),
                'workName':    Charstring().assignValueType(CharstringValue("WorkName"))
            })

            aComponent.mPort.send(executeWorkAnnouncement)
        else:
            # TODO: Raise a meaningful exception.
            raise

class Function_DetermineWorkCycleRequestResponse(Function):
    def __init__(self):
        self.mRunsOn = Component_Cribrarian_Cribrarian1

    def __call__(self, aComponent):
        if isinstance(aComponent, self.mRunsOn):
            cribrarian1 = {
                'type': Charstring().assignValueType(CharstringValue("Cribrarian")),
                'nick': Charstring().assignValueType(CharstringValue("Cribrarian1"))
            }

            worker1 = {
                'type': Charstring().assignValueType(CharstringValue("Worker")),
                'nick': Charstring().assignValueType(CharstringValue("Worker1"))
            }

            determineWorkCycleRequest = PiewikDetermineWorkCycleRequest()
            determineWorkCycleRequest.assignValueType({
                'messageName': Charstring().assignValueType(CharstringValue("DetermineWorkCycleRequest")),
                'sender':      worker1,
                'graphName':   Charstring().assignValueType(CharstringValue("GraphName")),
                'cycle':       Integer().assignValueType(IntegerValue(22)),
                'workName':    Charstring().assignValueType(CharstringValue("WorkName"))
            })

            determineWorkCycleResponse = PiewikDetermineWorkCycleResponse()
            determineWorkCycleResponse.assignValueType({
                'messageName': Charstring().assignValueType(CharstringValue("DetermineWorkCycleResponse")),
                'sender':      cribrarian1,
                'receiver':    worker1,
                'graphName':   Charstring().assignValueType(CharstringValue("GraphName")),
                'cycle':       Integer().assignValueType(IntegerValue(22)),
                'workName':    Charstring().assignValueType(CharstringValue("WorkName")),
                'workCycle':   Integer().assignValueType(IntegerValue(484))
            })

            aComponent.executeBlockingAction(
                Blocking(PortReceiveExpectation(aComponent.mPort, determineWorkCycleRequest)),
            )

            aComponent.mPort.send(determineWorkCycleResponse)
        else:
            # TODO: Raise a meaningful exception.
            raise

class Function_AwaitReportFinishedWorkAnnouncement(Function):
    def __init__(self):
        self.mRunsOn = Component_GraphYeeti_GraphYeeti1

    def __call__(self, aComponent):
        if isinstance(aComponent, self.mRunsOn):
            # TODO: Should wait until the components know each other. Remove this hardcoded value.
            time.sleep(1)

            worker1 = {
                'type': Charstring().assignValueType(CharstringValue("Worker")),
                'nick': Charstring().assignValueType(CharstringValue("Worker1"))
            }

            reportFinishedWorkAnnouncement = PiewikReportFinishedWorkAnnouncement()
            reportFinishedWorkAnnouncement.addAcceptDecorator(TemplateAcceptDecorator, {})
            reportFinishedWorkAnnouncement.assignValueType({
                'messageName': Charstring().assignValueType(CharstringValue("ReportFinishedWorkAnnouncement")),
                'sender':      worker1,
                'graphName':   Charstring().assignValueType(CharstringValue("GraphName")),
                'graphCycle':  Integer().assignValueType(IntegerValue(22)),
                'workName':    Charstring().assignValueType(CharstringValue("WorkName")),
                'workCycle':   Integer().assignValueType(IntegerValue(484)),
                'result':      TemplateBoolean().assignValueType(AnyValue())
            })

            aComponent.executeBlockingAction(
                Blocking(PortReceiveExpectation(aComponent.mPort, reportFinishedWorkAnnouncement)),
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

class Component_Balancer_Balancer1(Component):
    def __init__(self, aName):
        Component.__init__(self, aName)
        self.mPort = PiewikPort(self.mEventQueue)

class Component_Cribrarian_Cribrarian1(Component):
    def __init__(self, aName):
        Component.__init__(self, aName)
        self.mPort = PiewikPort(self.mEventQueue)

class Component_GraphYeeti_GraphYeeti1(Component):
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
        componentBalancer = Component_Balancer_Balancer1("Balancer")
        componentCribrarian = Component_Cribrarian_Cribrarian1("Cribrarian")
        componentGraphYeeti = Component_GraphYeeti_GraphYeeti1("GraphYeeti")

        componentBalancer.setContext(self.mMtc, self)
        componentCribrarian.setContext(self.mMtc, self)
        componentGraphYeeti.setContext(self.mMtc, self)

        componentBalancer.addFunction(Function_SendExecuteWorkAnnouncement())
        componentCribrarian.addFunction(Function_DetermineWorkCycleRequestResponse())
        componentGraphYeeti.addFunction(Function_AwaitReportFinishedWorkAnnouncement())

        componentBalancer.start()
        componentCribrarian.start()
        componentGraphYeeti.start()

        self.mMtc.executeBlockingAction(
            Interleave([
                Blocking(ComponentDoneExpectation(componentBalancer)),
                Blocking(ComponentDoneExpectation(componentCribrarian)),
                Blocking(ComponentDoneExpectation(componentGraphYeeti))
            ])
        )

testcase = SimpleTestcase()
control = Control()
control.execute(testcase)
