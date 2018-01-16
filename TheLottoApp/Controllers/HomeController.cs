using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace TheLottoApp.Controllers
{
    public class HomeController : Controller
    {
        public ActionResult Index()
        {
            
            return View();
        }

        public ActionResult About()
        {
            ViewBag.Message = "Your application description page.";

            return View();
        }

        public ActionResult Contact()
        {
            ViewBag.Message = "Your contact page.";

            return View();
        }
        public ActionResult HomeBanner()
        {
            return View();
        }
        public ActionResult AboutHomeCard ()
        {
            return View();
        }
        public ActionResult HomeCard()
        {
            return View();
        }
        public ActionResult HomeCardAlter()
        {
            return View();
        }
        public ActionResult RHSComponent()
        {
            return View();
        }
        public ActionResult SecurityHomeCard()
        {
            return View();
        }
    }
}