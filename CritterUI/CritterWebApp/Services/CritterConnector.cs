using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Web;
using ZeroMQ;
using CritterWebApp;
using ProtoBuf;
using System.IO;
using Critter.Messages;
using Google.ProtocolBuffers;

namespace CritterWebApp.Services
{      

    public class CritterConnector : BaseService
    {
        private ZmqSocket _CritterSubscriber;        
        private string _CritterNetworkURL;

        public CritterConnector()
        {
            this._CritterNetworkURL = "tcp://192.168.0.139:5555";
            ZmqContext Context = ZmqContext.Create();            
            this._CritterSubscriber = Context.CreateSocket(SocketType.REQ);            
        }

        static void Sample()
        {
            //byte[] bytes;
            ////Create a builder to start building a message
            //Person.Builder newContact = Person.CreateBuilder();
            ////Set the primitive properties
            //newContact.SetId(1)
            //          .SetName("Foo")
            //          .SetEmail("foo@bar");
            ////Now add an item to a list (repeating) field
            //newContact.AddPhone(
            //    //Create the child message inline
            //    Person.Types.PhoneNumber.CreateBuilder().SetNumber("555-1212").Build()
            //    );
            ////Now build the final message:
            //Person person = newContact.Build();
            ////The builder is no longer valid (at least not now, scheduled for 2.4):
            //newContact = null;
            //using (MemoryStream stream = new MemoryStream())
            //{
            //    //Save the person to a stream
            //    person.WriteTo(stream);
            //    bytes = stream.ToArray();
            //}
            ////Create another builder, merge the byte[], and build the message:
            //Person copy = Person.CreateBuilder().MergeFrom(bytes).Build();

            ////A more streamlined approach might look like this:
            //bytes = AddressBook.CreateBuilder().AddPerson(copy).Build().ToByteArray();
            ////And read the address book back again
            //AddressBook restored = AddressBook.CreateBuilder().MergeFrom(bytes).Build();
            ////The message performs a deep-comparison on equality:
            //if (restored.PersonCount != 1 || !person.Equals(restored.PersonList[0]))
            //    throw new ApplicationException("There is a bad person in here!");
        }
        
        public string PokeCreaterNetwork()
        {
            this._CritterSubscriber.Connect(this._CritterNetworkURL);
            
            //Announcment_Poke Poke = new Announcment_Poke();
            //Poke.messageName = "Announcment_Poke";
            //Poke.crittnick = "2";


            Command_DescribeCrittwork_Req.Builder reqBuilder = Command_DescribeCrittwork_Req.CreateBuilder();
            reqBuilder.SetCritthash("12345").SetMessageName("Command_DescribeCrittwork_Req");
            Command_DescribeCrittwork_Req req = reqBuilder.Build();

            Header.Builder envHeaderBuilder = Header.CreateBuilder();
            envHeaderBuilder.SetId(32);
            Header envHeader = envHeaderBuilder.Build();

            Payload.Builder envPayloadBuilder = Payload.CreateBuilder();
            envPayloadBuilder.SetPayload_(req.ToByteString());
            Payload envPayload = envPayloadBuilder.Build();

            Envelope.Builder envelopeBuilder = Envelope.CreateBuilder();
            envelopeBuilder.SetHeader(envHeader).SetPayload(envPayload);
            Envelope envelope = envelopeBuilder.Build();

            var message = envelope.ToByteString().ToString(Encoding.UTF8);
                                                          
            this._CritterSubscriber.Send(message, Encoding.UTF8);

            //Receive
            

            var received = this._CritterSubscriber.Receive(Encoding.UTF8);

            var receivedBytes = ByteString.CopyFromUtf8(received);

            Envelope restored = Envelope.CreateBuilder().MergeFrom(receivedBytes).Build();

            Command_DescribeCrittwork_Res response = Command_DescribeCrittwork_Res.CreateBuilder().MergeFrom(restored.Payload.Payload_).Build();


            return response.Dummy;

        }

    }
}