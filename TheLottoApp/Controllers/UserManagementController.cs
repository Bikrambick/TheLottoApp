using Microsoft.AspNet.Identity;
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
        public ActionResult Index()
        {
            return View();
        }
        public ActionResult MyProfile()
        {
            var userId = User.Identity.GetUserId();
            var model = new MyProfileViewModel();
            ApplicationDbContext context = new ApplicationDbContext();
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
    }
}