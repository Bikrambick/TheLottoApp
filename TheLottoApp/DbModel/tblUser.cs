//------------------------------------------------------------------------------
// <auto-generated>
//     This code was generated from a template.
//
//     Manual changes to this file may cause unexpected behavior in your application.
//     Manual changes to this file will be overwritten if the code is regenerated.
// </auto-generated>
//------------------------------------------------------------------------------

namespace TheLottoApp.DbModel
{
    using System;
    using System.Collections.Generic;
    
    public partial class tblUser
    {
        public string UserName { get; set; }
        public string Password { get; set; }
        public string Email { get; set; }
        public string Phone { get; set; }
        public string SelectedPlan { get; set; }
        public Nullable<double> UserType { get; set; }
        public Nullable<System.DateTime> DOB { get; set; }
        public Nullable<int> NbWon { get; set; }
        public string WealthEst { get; set; }
    }
}
