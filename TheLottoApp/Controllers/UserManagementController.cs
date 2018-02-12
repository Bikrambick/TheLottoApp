﻿using Microsoft.AspNet.Identity;
using Microsoft.AspNet.Identity.EntityFramework;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using TheLottoApp.Models;

namespace TheLottoApp.Controllers
{
    public class UserManagementController : Controller
    {
        // GET: UserManagement
        ApplicationDbContext context = new ApplicationDbContext();
        public ActionResult Index()
        {
            return View();
        }
        public ActionResult MyProfile()
        {
            var userId = User.Identity.GetUserId();
            var model = new MyProfileViewModel();
            
            if (userId != null)
            {
                using(var dbContext = new TheLottoAppDbEntity())
                {
                    
                    var userStore = new UserStore<ApplicationUser>(context);
                    var userManager = new UserManager<ApplicationUser>(userStore);
                    var Subscription = userManager.GetRoles(userId);
                    try
                    {
                        var results = from x in dbContext.AspNetUsers
                                      where x.Id == userId
                                      select new MyProfileViewModel
                                      {
                                          UserName = x.Email,
                                          DateOfBirth = (DateTime?)x.DOB.Value ?? DateTime.Now,
                                          TotalWin = (int?)x.NbWon.Value ?? 0,
                                          TotalNumberGenerated = (int?)x.TotalNumberGenerated.Value ?? 0,
                                          LastGeneratedNumber = (DateTime?)x.LastGeneratedNumber.Value ?? DateTime.Now,
                                          Subscription = Subscription.FirstOrDefault()
                                      } ;
                        return View(results.ToList());
                    }
                    catch(Exception ex) { }
                   

                    

                    
                }
            }

            return View("../Account/Login");
           
        }
        public void SetGeneratedNumberSet(object userId, int totalTickets)
        {
            using (var db = new TheLottoAppDbEntity())
            {
                var genSetModel = new tblUserGeneratedTicket();
                genSetModel.User_Id = userId.ToString();
                genSetModel.Total_Tickets_Generated = totalTickets;
                genSetModel.Ticket_Generated_Date = DateTime.Now;
                db.tblUserGeneratedTickets.Add(genSetModel);
                try
                {
                    db.SaveChanges();
                }
                catch (Exception ex) { }
            }
        }
        public int GetGeneratedNumberSet(object userId)
        {
            using (var db = new TheLottoAppDbEntity())
            {
                //if today is monday then straight to total allowed tickets else get last monday and then
                //get the sum of all generated tickets after monday.
                if(DateTime.Now.DayOfWeek == DayOfWeek.Monday)
                {

                    return 0;
                }
                else
                {
                    try
                    {
                        var Lastmonday = DateTime.Today.AddDays(-(int)DateTime.Today.DayOfWeek + (int)DayOfWeek.Monday);
                        var tkc = db.tblUserGeneratedTickets.Where(x => x.User_Id == userId.ToString()).
                            Where(x => x.Ticket_Generated_Date >= Lastmonday).GroupBy(x => x.Id).Select(x => x.Sum(y=>y.Total_Tickets_Generated));

                        return Convert.ToInt32(tkc.FirstOrDefault());
                     }
                    catch (Exception ex) { }
                }
            }
            return 0;
        }
        public string GetUserSusbription(string userId)
        {
            using (var db = new TheLottoAppDbEntity())
            {
                var userStore = new UserStore<ApplicationUser>(context);
                var userManager = new UserManager<ApplicationUser>(userStore);
                try
                {
                    var Subscription = userManager.GetRoles(userId);
                    return Subscription.FirstOrDefault().ToString();
                }
                catch(Exception ex) { }

                return "";
            }
        }
        public List<AspNetRole> GetUserSystem(string Subscription)
        {
            using (var db = new TheLottoAppDbEntity())
                try
                {

                    return db.AspNetRoles.Where(x => x.Name == Subscription).ToList();

                }
                catch (Exception ex) { }
            return null;
        }
        

        public void CheckSetWeeklyTicketAllownces(string email)
        {
            
            using (var db = new TheLottoAppDbEntity())
            {
                try
                {
                    var userId = db.AspNetUsers.Where(x => x.Email == email).Select(x => x.Id).FirstOrDefault();
                    var existingRecord = db.tblUserGeneratedTickets.Where(x => x.User_Id == userId.ToString()).SingleOrDefault();
                    if (existingRecord != null)
                    {
                        DateTime lastGeneratedDate = Convert.ToDateTime(existingRecord.Ticket_Generated_Date);
                        var DaysSinceLastGenerated = DateTime.Now.Subtract(lastGeneratedDate).TotalDays;
                        if (DaysSinceLastGenerated > 6)
                        {
                            existingRecord.Ticket_Generated_Date = DateTime.Now;
                            existingRecord.Total_Tickets_Generated = 0;
                            try
                            {
                                db.SaveChanges();
                            }
                            catch (Exception ex) { }
                        }
                    }
                }
                catch(Exception ex) { }
                
               
               
            }
        }

    }
}