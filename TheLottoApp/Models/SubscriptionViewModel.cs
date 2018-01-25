using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace TheLottoApp.Models
{
    public class SubscriptionViewModel
    {
        public int allowedTickets { get; set; }
        public string plan { get; set; }
        public double price { get; set; }
    }
}