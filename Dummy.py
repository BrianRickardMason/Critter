import time
import zmq

from Critter.Critter import Critter

context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://127.0.0.1:5555")

fakeCritter = Critter('HelloCritty', 'Fake', [])

messageName = 'Command_DescribeCrittwork_Req'
internalMessage = fakeCritter.mPostOffice.encode({
    'messageName': messageName,
    'critthash':   '12345'
})
envelope = fakeCritter.mPostOffice.putIntoAnEnvelope(internalMessage)
message = envelope.SerializeToString()

i = 0
while True:
    request = message
    socket.send(request)
    response = socket.recv()
    i+=1
    time.sleep(1)
