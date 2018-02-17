using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using DataAccess;
using TheLottoApp.Models;
using System.IO;
using Microsoft.AspNet.Identity;

namespace TheLottoApp.Controllers
{
    public class NumberGeneratorController : Controller
    {
        // GET: NumberGenerator
        public ActionResult Index()
        {
            return View();
        }

        public ActionResult ShowSelection()
        {

            return View();
        }
        public ActionResult Basic()
        {

            return View();
        }
        [HttpPost]
        public JsonResult GenerateBasic(BasicGeneratorModel model)
        {
            if (User.Identity.IsAuthenticated)
            {
                var userid = User.Identity.GetUserId();
                var rootPythonDir = Server.MapPath("../PyFiles/");
                var filePathHistory = Path.Combine(rootPythonDir, "ozzhistory.txt");
                var pathToLib = Server.MapPath("../PyFiles/Lib");
                var pathToPyFile = Server.MapPath("../PyFiles/baic_engine.py");
                DataAccess.BasicEngine IPyInterface = new BasicEngine(pathToLib, pathToPyFile,"ozlotto",filePathHistory);



                var userController = new UserManagementController();
                var userSubscription = userController.GetUserSusbription(userid.ToString());

                var userSystem = userController.GetUserSystem(userSubscription);

                int systemNumbers = Convert.ToInt32(userSystem.Select(x => x.Allowed_Numbers).FirstOrDefault()) + 1;
                var totalAllowedTicket = Convert.ToInt32(userSystem.Select(x => x.Allowed_Tickets).FirstOrDefault());

                int TotalTicketsToGenerated = 0;
                var PreviouslyGeneratedRecord = userController.GetGeneratedNumberSet(userid);
                try
                {
                    TotalTicketsToGenerated = Convert.ToInt32(userController.GetGeneratedNumberSet(userid));
                }
                catch (Exception ex) { }


                int RemainingTicketsThisWeek = totalAllowedTicket - (TotalTicketsToGenerated + model.NumberOfGames);
                string selectedStrategy = string.Empty;
                if (model.hotNumbers)
                {
                    selectedStrategy = "hot_numbers";
                }
                else if (model.zeroRepeats)
                {
                    selectedStrategy = "zero_prev_nb";
                }
                else if (model.bestScore)
                {
                    selectedStrategy = "best_score";
                }
                else
                {
                    selectedStrategy = "balanced";
                }
                List<List<int>> generatedSets = new List<List<int>>();
                List<int> GeneratedNumberSetEachGame = new List<int>();
                try
                {
                    //lottery_id,strategy_id, nb_of_tickets_left, nb_of_games, system, user_plan, file_path
                    var results = IPyInterface.CallFunction("get_set","ozlotto",selectedStrategy, RemainingTicketsThisWeek, model.NumberOfGames, model.system, 
                                                            userSubscription, filePathHistory);
                    if (results is string)
                    {
                        return Json(new { GeneratedSet = results }, JsonRequestBehavior.AllowGet);
                    }

                    if (results != null)
                    {

                        foreach (var item in results)
                        {
                            if (item is string) { return Json(new { GeneratedSet = item }, JsonRequestBehavior.AllowGet); }
                            if (item != null)
                            {
                                GeneratedNumberSetEachGame = new List<int>();
                                foreach (var itemX in item)
                                {
                                    if (itemX == null) continue;
                                    GeneratedNumberSetEachGame.Add(itemX);
                                }
                                generatedSets.Add(GeneratedNumberSetEachGame);
                            }



                        }

                        userController.SetGeneratedNumberSet(userid, model.NumberOfGames);

                    }
                    return Json(new { GeneratedSet = generatedSets }, JsonRequestBehavior.AllowGet);

                }
                catch(Exception ex) { }

            }
            else
            {
                return Json(new { GeneratedSet = "Please <a href = '../Account/Login'>Login</a> to Generate Number." }, JsonRequestBehavior.AllowGet);
            }

            return Json(new { GeneratedSet = "Server Error!!!" }, JsonRequestBehavior.AllowGet);
        }

        [HttpPost]
        public JsonResult GenerateNumber(NumberGeneratorViewModel model)
         {
            if (User.Identity.IsAuthenticated)
            {
                
                var rootPythonDir = Server.MapPath("../PyFiles/");
                var filePathHistory = Path.Combine(rootPythonDir, "ozzhistory.txt");
                var pathToLib = Server.MapPath("../PyFiles/Lib");
                var pathToPyFile = Server.MapPath("../PyFiles/twelve_version_for_iron_python.py");
                DataAccess.PythonInterface IPyInterface = new PythonInterface(pathToLib, pathToPyFile);
                var score_range = model.ScoreRange;
                var scorerange = score_range.Split(',');
                var one = double.Parse(scorerange[0]);
                var two = double.Parse(scorerange[1]);

                List<int> oddNumbers = new List<int>();
                if (model.oddNumberForZero == true) { oddNumbers.Add(0); }
                if (model.oddNumberForOne == true) { oddNumbers.Add(1); }
                if (model.oddNumberForTwo== true) { oddNumbers.Add(2); }
                if (model.oddNumberForThree == true) { oddNumbers.Add(3); }
                if (model.oddNumberForFour == true) { oddNumbers.Add(4); }
                if (model.oddNumberForFive == true) { oddNumbers.Add(5); }
                if (model.oddNumberForSix == true) { oddNumbers.Add(6); }
                if (model.oddNumberForSeven == true) { oddNumbers.Add(7); }

                double[] ScoreVeryRange = { one, two };
                object userid = 0;
                //var lottery = model.LottoId; 
                var lottery = "ozlotto";
                try
                {

                    userid = User.Identity.GetUserId();

                }
                catch(Exception ex) { }

                //get previously generated record to pass to python
                
                var userController = new UserManagementController();
                var userSubscription = userController.GetUserSusbription(userid.ToString());

                var userSystem = userController.GetUserSystem(userSubscription);
                
                int systemNumbers = Convert.ToInt32(userSystem.Select(x => x.Allowed_Numbers).FirstOrDefault())+1;
                if (model.system > systemNumbers)
                {
                    return Json(new { GeneratedSet = "Your chose exceeds the quota!!!" }, JsonRequestBehavior.AllowGet);
                }

                var totalAllowedTicket = Convert.ToInt32(userSystem.Select(x => x.Allowed_Tickets).FirstOrDefault());

                int TotalTicketsToGenerated = 0;
                //var PreviouslyGeneratedRecord = userController.GetGeneratedNumberSet(userid);
                try
                {
                    TotalTicketsToGenerated = Convert.ToInt32(userController.GetGeneratedNumberSet(userid));
                }
                catch(Exception ex) { }
                
                
                int RemainingTicketsThisWeek = totalAllowedTicket-(TotalTicketsToGenerated + model.NumberOfGames);




                //var numberOfOdds = model.NumberOfOdds;
                int flag_for_odds = 0;
                //if (model.NumberOfOdds == -1)
                //{
                //    flag_for_odds = 0;
                //}

                if ((model.oddNumberForIgnore == true) || (model.oddNumberForZero == false && model.oddNumberForOne == false && model.oddNumberForTwo == false && model.oddNumberForThree == false && model.oddNumberForFour == false && model.oddNumberForFive == false && model.oddNumberForSix == false && model.oddNumberForSeven == false && model.oddNumberForIgnore == false))
                {
                    flag_for_odds = 0;
                } 

                else { flag_for_odds = 1; }

                var nb_less_15 = model.NumbersBelow15;
                int flag_for_15 = 0;
                if (model.NumbersBelow15 == 0)
                {
                    flag_for_15 = 0;
                }
                else { flag_for_15 = 1; }

                var nb_middle = model.NumbersBelow15And30;
                int flag_middle = 0;

                if (model.NumbersBelow15And30 == 0)
                {
                    flag_middle = 0;
                }
                else { flag_middle = 1; }


                var nb_bigger_30 = model.NumbersAbove30;
                int flag_for_30 = 0;
                if (model.NumbersAbove30 == 0)
                {
                    flag_for_30 = 0;
                }
                else { flag_for_30 = 1; }

                // List<double> score_range = new List<double> { 0.01, 0.03 };
                var flag_for_score_range = 0;
                if (string.IsNullOrEmpty(model.ScoreRange) || model.ScoreRange == "0.018,0.028")
                {
                    flag_for_score_range = 0;
                }
                else { flag_for_score_range = 1; }
                var prev_rep_numb = model.NumbersOfPreviousRepeat;
                var flag_for_prev_num = 0;
                if (model.NumbersOfPreviousRepeat == 0)
                {
                    flag_for_prev_num = 0;
                }
                else { flag_for_prev_num = 1; }
                string nb_to_inc = string.Empty;
                if (string.IsNullOrEmpty(model.NumbersToInclude))
                {
                    nb_to_inc = "";
                }
                else
                {
                    nb_to_inc = model.NumbersToInclude;
                }
                string nb_to_excl = string.Empty;
                if (string.IsNullOrEmpty(model.NumbersToExclude))
                {
                    nb_to_excl = "";
                }
                else
                {
                    nb_to_excl = model.NumbersToExclude;
                }

                var nb_of_games = model.NumberOfGames;
                List<List<int>> generatedSets = new List<List<int>>();
                List<int> GeneratedNumberSetEachGame = new List<int>();
                try
                {
                    var results = IPyInterface.CallFunction("get_set", lottery, userid, oddNumbers, flag_for_odds
                                     , nb_less_15, flag_for_15, nb_middle, flag_middle, nb_bigger_30, flag_for_30
                                     , ScoreVeryRange, flag_for_score_range, prev_rep_numb, flag_for_prev_num
                                     , nb_to_inc, nb_to_excl, nb_of_games, filePathHistory,RemainingTicketsThisWeek, model.system, userSubscription);
                    if (results is string)
                    {
                        return Json(new { GeneratedSet = results }, JsonRequestBehavior.AllowGet);
                    }

                    if (results != null)
                    {

                        foreach (var item in results)
                        {
                            if (item is string) { return Json(new { GeneratedSet = item }, JsonRequestBehavior.AllowGet); }
                            if (item != null)
                            {
                                GeneratedNumberSetEachGame = new List<int>();
                                foreach (var itemX in item)
                                {
                                    if (itemX == null) continue;
                                    GeneratedNumberSetEachGame.Add(itemX);
                                }
                                generatedSets.Add(GeneratedNumberSetEachGame);
                            }

                            

                        }

                       userController.SetGeneratedNumberSet(userid, model.NumberOfGames);

                    }
                    return Json(new { GeneratedSet = generatedSets }, JsonRequestBehavior.AllowGet);
                }
                catch (Exception ex) { }
            }
            else
            {
                return Json(new { GeneratedSet = "Please <a href = '../Account/Login'>Login</a> to Generate Numbers." }, JsonRequestBehavior.AllowGet);
            }
           
            return Json(new { GeneratedSet = "Server Error!!!" }, JsonRequestBehavior.AllowGet);
        }
       
    }
}