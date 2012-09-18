using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Web.Routing;

namespace CritterWebApp.Controllers
{
    public class CritterController : Controller
    {
        public string ActionName { get; set; }
        public string ControllerName { get; set; }
        public string PageTitle { get; set; }

        protected override void Initialize(RequestContext Context)  
        {
            base.Initialize(Context);
            this.ActionName = Context.RouteData.GetRequiredString("action");
            this.ControllerName = Context.RouteData.GetRequiredString("controller");
            this.PageTitle = !this.ActionName.Equals("Index") ? this.ActionName : this.ControllerName;           
        }
    }
}
