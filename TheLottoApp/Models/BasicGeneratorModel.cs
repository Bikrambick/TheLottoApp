using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace TheLottoApp.Models
{
    public class BasicGeneratorModel
    {
        public int NumberOfGames { get; set; }
        public int system { get; set; }
        public bool hotNumbers { get; set; }
        public bool zeroRepeats { get; set; }
        public bool bestScore { get; set; }
        public bool balanced { get; set; }
    }
}