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
    
    public partial class tblGeneratedSet
    {
        public string Lottery { get; set; }
        public Nullable<System.DateTime> DateTime { get; set; }
        public string UserName { get; set; }
        public Nullable<int> NbOfOdds { get; set; }
        public Nullable<bool> FlagForOdds { get; set; }
        public Nullable<int> Timing { get; set; }
        public Nullable<int> NbOfB20 { get; set; }
        public Nullable<bool> FlagForB20 { get; set; }
        public Nullable<int> ScoreRangeTop { get; set; }
        public Nullable<int> ScoreRangeBottom { get; set; }
        public Nullable<bool> FlagForScore { get; set; }
        public Nullable<double> SetScore { get; set; }
        public Nullable<double> PrevRepNb { get; set; }
        public Nullable<bool> FlagForPrevRep { get; set; }
        public string NbToInc { get; set; }
        public Nullable<double> NbOfGames { get; set; }
        public Nullable<bool> FailedFlag { get; set; }
        public int SetID { get; set; }
    }
}
