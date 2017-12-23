using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace TheLottoApp.Models
{
    public class CharGeneratorModel
    {
        public Dictionary<int,int> NumbersStat { get; set; }
        public Dictionary<int, double> PrevRepeated { get; set; }
        public Dictionary<int, double> PreviousOdd { get; set; }
        public Dictionary<string, double> PreviousRange { get; set; }
        public List<double> ScoreChart { get; set; }
        public List<double> TimeScore { get; set; }

    }
}