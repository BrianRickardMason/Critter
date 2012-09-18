using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace CritterWebApp.Controllers
{
    public class AccountController : CritterController
    {     
       
        [HttpGet]        
        public ActionResult Dashboard()
        {
            ViewBag.Title = this.PageTitle;
            return View();
        }
       
    }
}
