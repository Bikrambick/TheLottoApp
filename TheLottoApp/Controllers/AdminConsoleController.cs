using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace TheLottoApp.Controllers
{
    public class AdminConsoleController : Controller
    {
        // GET: AdminConsole
        public ActionResult Index()
        {
            return View();
        }
        public ActionResult EnterWinningNumbers()
        {
            return View();
        }
        [HttpPost]
        public ActionResult EnterWinningNumbers(tblLottoHistory HistoryModel)
        {
            var db = new TheLottoAppDbEntity();
                
                
            var tableModel = new tblLottoHistory();
            tableModel.Draw_Date = HistoryModel.Draw_Date;
            tableModel.Lotto_Id = HistoryModel.Lotto_Id;
            tableModel.Winning_Numbers = HistoryModel.Winning_Numbers;
            db.tblLottoHistories.Add(tableModel);
                
            try
            {
                var results = db.SaveChanges();
            }catch(Exception ex) { }
            
            return View();
        }
    }
}