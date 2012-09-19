using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using CritterWebApp.Services;
using CritterWebApp.ViewModels;

namespace CritterWebApp.Controllers
{
    public class ReportsController : CritterController
    {
        //
        // GET: /Reports/

        public ActionResult Index()
        {
            DateTime start = DateTime.Now;

            ViewBag.Title = this.PageTitle;
            CritterConnector Conector = new CritterConnector();
            string message =  Conector.PokeCreaterNetwork();
            ReportsIndexViewModel viewModel = new ReportsIndexViewModel();
            viewModel.Message = message;            

            var ts = DateTime.Now.Subtract(start).TotalSeconds;
            viewModel.ExecutionTime = ts;

            return View(viewModel);
        }

    }
}
