﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace CritterWebApp.Controllers
{
    public class JobsController : CritterController
    {
        //
        // GET: /Jobs/

        public ActionResult Index()
        {
            ViewBag.Title = this.PageTitle;
            return View();
        }

    }
}
