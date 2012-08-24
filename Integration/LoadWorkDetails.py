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

            cribrarian1 = {
                'type': Charstring().assignValueType(CharstringValue("Cribrarian")),
                'nick': Charstring().assignValueType(CharstringValue("Cribrarian1"))
            }

            worker1 = {
                'type': Charstring().assignValueType(CharstringValue("Worker")),
                'nick': Charstring().assignValueType(CharstringValue("Worker1"))
            }

            loadWorkDetailsRequest = PiewikLoadWorkDetailsRequest()
            loadWorkDetailsRequest.assignValueType({
                'messageName': Charstring().assignValueType(CharstringValue("LoadWorkDetailsRequest")),
                'sender':      worker1
            })

            # TODO: Should be verified in a more detailed way.
            loadWorkDetailsResponse = PiewikLoadWorkDetailsResponse()
            loadWorkDetailsResponse.addAcceptDecorator(TemplateAcceptDecorator, {})
            loadWorkDetailsResponse.assignValueType({
                'messageName': Charstring().assignValueType(CharstringValue("LoadWorkDetailsResponse")),
                'sender':      cribrarian1,
                'receiver':    worker1,
                'details':     AnyValueType()
            })

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
