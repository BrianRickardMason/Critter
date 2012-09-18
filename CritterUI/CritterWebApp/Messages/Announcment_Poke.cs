using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using ProtoBuf;

namespace CritterWebApp.Messages
{
    [ProtoContract]
    public class Announcment_Poke
    {
        [ProtoMember(1)]
        public string messageName { get; set; }
        [ProtoMember(2)]
        public string crittnick { get; set; }        
    }
}