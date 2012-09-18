using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Web;
using ZeroMQ;
using CritterWebApp.Messages;
using ProtoBuf;
using System.IO;

namespace CritterWebApp.Services
{      

    public class CritterConnector : BaseService
    {
        private ZmqSocket _CritterSubscriber;
        private string _CritterNetworkURL;

        public CritterConnector()
        {
            this._CritterNetworkURL = "tcp://192.168.0.139:2222";
            ZmqContext Context = ZmqContext.Create();            
            this._CritterSubscriber = Context.CreateSocket(SocketType.REQ);                            
        }
        
        public void PokeCreaterNetwork()
        {
            this._CritterSubscriber.Connect(this._CritterNetworkURL);
            
            Announcment_Poke Poke = new Announcment_Poke();
            Poke.messageName = "Announcment_Poke";
            Poke.crittnick = "2";
            
            var PokeMessage = new MemoryStream();
            
            Serializer.Serialize<Announcment_Poke>(PokeMessage, Poke);
           
            StreamReader sr = new StreamReader(PokeMessage);
            char[] str = new char[sr.BaseStream.Length];
            
            
            //PokeMessage = File.Open("Messages/Announcment_Poke.bin", FileMode.Open);
            //byte[] PokeMessageBytes = Encoding.ASCII.GetBytes("Test");
            
            //PokeMessage.Read(PokeMessageBytes, 0, Convert.ToInt32(PokeMessage.Length));
            //PokeMessage.Close();
            
            //this._CritterSubscriber.Send(PokeMessageBytes);
            
            this._CritterSubscriber.Send("Hellow",Encoding.Unicode);

        }

    }
}