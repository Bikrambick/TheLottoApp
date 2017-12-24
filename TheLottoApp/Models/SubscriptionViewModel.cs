using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace TheLottoApp.Models
{
    public class SubscriptionViewModel
    {
        public string plan { get; set; }
        public double price { get; set; }
        public int allowedTickets { get; set; }
    }
}