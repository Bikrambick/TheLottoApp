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
    
    public partial class tblResult
    {
        public Nullable<int> LotteryID { get; set; }
        public Nullable<System.DateTime> ResultDate { get; set; }
        public string NumberSet { get; set; }
        public int ResultID { get; set; }
    
        public virtual tblLottery tblLottery { get; set; }
    }
}
