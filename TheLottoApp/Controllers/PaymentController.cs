using Stripe;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace TheLottoApp.Controllers
{
    public class PaymentController : Controller
    {
        // GET: Payment
        public ActionResult Index()
        {
            var stripePublishKey = ConfigurationManager.AppSettings["stripePublishableKey"];
            ViewBag.StripePublishKey = stripePublishKey;
            return View();
            
        }
        [HttpPost]
        public ActionResult Charge(string stripeEmail, string stripeToken,int amount)
        {
            //use selected plan argument to set amount to charge 
            var customers = new StripeCustomerService();
            var charges = new StripeChargeService();
            StripeConfiguration.SetApiKey("sk_test_I8IpHbhCWX5Qdb4lbiOELpcO");
            var customer = customers.Create(new StripeCustomerCreateOptions
            {
                Email = stripeEmail,
                SourceToken = stripeToken
            });
            
            try
            {
                var charge = charges.Create(new StripeChargeCreateOptions
                {
                    Amount = amount,//charge in cents
                    Description = "Subscription Charge",
                    Currency = "aud",
                    CustomerId = customer.Id
                });
                String SelectedSubscription = string.Empty;
                int caseSwitch = amount;
                switch (caseSwitch)
                {
                    case 500:
                        SelectedSubscription = "Basic";
                        break;
                    case 2500:
                        SelectedSubscription = "Standard";
                        break;
                    case 4500:
                        SelectedSubscription = "Professional";
                        break;
                    default:
                        SelectedSubscription = "Platinum";
                        break;
                }



                AccountController oController = new AccountController();
                if (oController.CreateUserAddRolePostPayment(stripeEmail, "SomeRandomP@ssword123", SelectedSubscription))
                    return View("../Manage/SetPassword");
                
                
               
            }
            catch(Exception ex) { }
            

            // further application specific code goes here

            return View("../Manage/SetPassword");
        }
    }
}