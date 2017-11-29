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
        //public void TestPythonInterface()
        //{
        //    var rootPythonDir = Server.MapPath("../PyFiles/");
        //    var pathToLib = Server.MapPath("../PyFiles/Lib");
        //    var pathToPyFile = Server.MapPath("../PyFiles/twelve_version_for_iron_python.py");
        //    DataAccess.PythonInterface IPyInterface = new PythonInterface(pathToLib,pathToPyFile);
        //    try
        //    {
        //        var result = IPyInterface.CallFunction("get_set");
        //    }catch(Exception ex) { }
        //}
        [HttpPost]
        public void GenerateNumber()
        {
            var rootPythonDir = Server.MapPath("../PyFiles/");
            var pathToLib = Server.MapPath("../PyFiles/Lib");
            var pathToPyFile = Server.MapPath("../PyFiles/twelve_version_for_iron_python.py");
            DataAccess.PythonInterface IPyInterface = new PythonInterface(pathToLib, pathToPyFile);

            var lottery = "ozlotto";
            var userid = 98765;
            var numberOfOdds = 3;
            var flag_for_odds = 0;
            var nb_less_15 = 0;
            var flag_for_15 = 0;
            var nb_middle = 0;
            var flag_middle = 0;
            var nb_bigger_30 = 0;
            var flag_for_30 = 0;
            List<double> score_range = new List<double> { 0.01, 0.03 };
            var flag_for_score_range = 0;
            var prev_rep_numb = 0;
            var flag_for_prev_num = 0;
            var nb_to_inc = "45";
            var nb_to_excl = "1";
            var nb_of_games = 20;
            try
            {
                var result = IPyInterface.CallFunction("get_set", lottery, userid, numberOfOdds, flag_for_odds
                                 , nb_less_15, flag_for_15, nb_middle, flag_middle, nb_bigger_30, flag_for_30
                                 , score_range, flag_for_score_range, prev_rep_numb, flag_for_prev_num
                                 , nb_to_inc, nb_to_excl, nb_of_games);
            }
            catch (Exception ex) { }
        }
    }
}