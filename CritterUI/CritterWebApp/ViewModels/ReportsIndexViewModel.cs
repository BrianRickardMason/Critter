using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace CritterWebApp.ViewModels
{
    public class ReportsIndexViewModel : BaseViewModel
    {
        private String _message;
        private double _executionTime;

        public double ExecutionTime
        {
            get { return _executionTime; }
            set { _executionTime = value; }
        }

        public String Message
        {
            get { return _message; }
            set { _message = value; }
        }

        public ReportsIndexViewModel()
        {
 
        }
    }
}