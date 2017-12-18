using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace TheLottoApp.Models
{
    public class MyProfileViewModel
    {
        public string UserName { get; set; }
        public DateTime DateOfBirth { get; set; }
        public int TotalWin { get; set; }
        public int TotalNumberGenerated { get; set; }
        public DateTime LastGeneratedNumber { get; set; }
        public string Subscription { get; set; }

    }
}