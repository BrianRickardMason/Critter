using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace CritterWebApp.ViewModels
{
    public class BaseViewModel
    {
        private string _userType;
        public string ControllerName { get; set; }
        public string ActionName { get; set; }
        public string UserType 
        { 
            get 
            { 
                if( _userType == null ){
                    return "Guest";
                }
                return _userType;
            }
            set
            {
                _userType = value;
            } 
        }
    }
}