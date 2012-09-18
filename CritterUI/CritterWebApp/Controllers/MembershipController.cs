using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace CritterWebApp.Controllers
{
    public class MembershipController : CritterController
    {
        //
        // GET: /Membership/

        public ActionResult Login()
        {
            ViewBag.Title = this.PageTitle;
            return View();
        }

    }
}
