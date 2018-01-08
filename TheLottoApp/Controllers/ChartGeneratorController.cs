using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace TheLottoApp.Controllers
{
    public class ChartGeneratorController : Controller
    {
        // GET: ChartGenerator
        public ActionResult Index()
        {
            return View();
        }
        [HttpPost]
        public JsonResult GenerateChart()
        {
            if (User.Identity.IsAuthenticated)
            {
                var rootPythonDir = Server.MapPath("../PyFiles/");
                var filePathHistory = Path.Combine(rootPythonDir, "ozzhistory.txt");
                var pathToLib = Server.MapPath("../PyFiles/Lib");
                var pathToPyFile = Server.MapPath("../PyFiles/stastic_engine.py");
                List<object> chartDataBallOccurance = new List<object>();
                List<object> chartDataPreviousRepeat = new List<object>();
                List<object> chartDataPreviousOdd = new List<object>();
                List<List<object>> ChartDataCollection = new List<List<object>>();
                DataAccess.ChartFromStat IChartFromStat = new DataAccess.ChartFromStat(pathToLib, pathToPyFile, "ozlotto", filePathHistory);
                try
                {
                    //IChartFromStat = new DataAccess.ChartFromStat(pathToLib, pathToPyFile, "ozlotto", filePathHistory);
                    var numbersStat = IChartFromStat.CallFunction("get_numbers_statistict");
                    if (numbersStat is string)
                    {
                        return Json(new { GeneratedSet = numbersStat }, JsonRequestBehavior.AllowGet);
                    }

                    //load ball occurance
                    chartDataBallOccurance = LoadchartDataBallOccurance(numbersStat);
                    ChartDataCollection.Add(chartDataBallOccurance);

                    
                    var prevRepeat = IChartFromStat.CallFunction("get_prev_repeated");
                    if (prevRepeat is string)
                    {
                        return Json(new { GeneratedSet = prevRepeat }, JsonRequestBehavior.AllowGet);
                    }
                     
                    //load Previous repeat
                    chartDataPreviousRepeat = LoadchartDataPreviousRepeat(prevRepeat);
                    ChartDataCollection.Add(chartDataPreviousRepeat);


                    
                    var prevOdd = IChartFromStat.CallFunction("get_nb_of_odds");
                    if (prevOdd is string)
                    {
                        return Json(new { GeneratedSet = prevOdd }, JsonRequestBehavior.AllowGet);
                    }
                    //load previous odd
                    chartDataPreviousOdd = LoadchartDataPreviousOdd(prevOdd);
                    ChartDataCollection.Add(chartDataPreviousOdd);
                }
                catch(Exception ex) { }
                return Json(ChartDataCollection);
            }
            
            return Json(new { GeneratedSet = "Server Error!!!" }, JsonRequestBehavior.AllowGet);
        }
        private List<object> LoadchartDataBallOccurance(dynamic results)
        {
            List<object> chartDataBallOccurance = new List<object>();
            chartDataBallOccurance.Add(new object[]
                                    {
                                    "Ball", "TotalOccurance"
                                    });

            foreach (var item in results)
            {
                var ball = item;
                var occurance = results[item];
                chartDataBallOccurance.Add(new object[]
                {
                            ball.ToString(), occurance
                });
            }
            return chartDataBallOccurance;
        }
        private List<object> LoadchartDataPreviousRepeat(dynamic results)
        {
            List<object> chartDataPreviousRepeat = new List<object>();
            chartDataPreviousRepeat.Add(new object[]
                                    {
                                    "Ball", "Repeated times"
                                    });

            foreach (var item in results)
            {
                var ball = item;
                var occurance = results[item];
                chartDataPreviousRepeat.Add(new object[]
                {
                            ball.ToString(), occurance
                });
            }



            return chartDataPreviousRepeat;
        }
        private List<object> LoadchartDataPreviousOdd(dynamic results)
        {
            List<object> chartDataPreviousOdd = new List<object>();
            chartDataPreviousOdd.Add(new object[]
                                    {
                                    "Ball", "Repeated times"
                                    });

            foreach (var item in results)
            {
                var ball = item;
                var occurance = results[item];
                chartDataPreviousOdd.Add(new object[]
                {
                            ball.ToString(), occurance
                });
            }



            return chartDataPreviousOdd;
        }
    }
}