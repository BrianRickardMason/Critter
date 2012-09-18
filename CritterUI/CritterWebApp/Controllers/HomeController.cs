using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace CritterWebApp.Controllers
{
    public class HomeController : CritterController
    {
        
        public ActionResult Index()
        {
            ViewBag.Title = this.PageTitle;
            return View();
        }
    }
}
