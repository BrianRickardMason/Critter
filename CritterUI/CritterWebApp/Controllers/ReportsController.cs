using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using CritterWebApp.Services;

namespace CritterWebApp.Controllers
{
    public class ReportsController : CritterController
    {
        //
        // GET: /Reports/

        public ActionResult Index()
        {
            ViewBag.Title = this.PageTitle;
            CritterConnector Conector = new CritterConnector();
            Conector.PokeCreaterNetwork();
            return View();
        }

    }
}
