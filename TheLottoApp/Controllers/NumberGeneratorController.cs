using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using DataAccess;
namespace TheLottoApp.Controllers
{
    public class NumberGeneratorController : Controller
    {
        // GET: NumberGenerator
        public ActionResult Index()
        {
            return View();
        }
        public void TestPythonInterface()
        {
            var rootPythonDir = Server.MapPath("../PyFiles/");
            var pathToLib = Server.MapPath("../PyFiles/Lib");
            var pathToPyFile = Server.MapPath("../PyFiles/twelve_version_for_iron_python.py");
            DataAccess.PythonInterface IPyInterface = new PythonInterface(pathToLib,pathToPyFile);
            try
            {
                var result = IPyInterface.CallFunction("get_the_first_chart");
            }catch(Exception ex) { }
        }
    }
}