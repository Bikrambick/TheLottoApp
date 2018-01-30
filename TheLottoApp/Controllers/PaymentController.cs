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
               
            }
            catch(Exception ex) { }
            

            // further application specific code goes here

            return View("../Account/Register");
        }
    }
}