using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace TheLottoApp.Controllers
{
    public class NumberGeneratorController : Controller
    {
        // GET: NumberGenerator
        public ActionResult Index()
        {
            return View();
        }
    }
}