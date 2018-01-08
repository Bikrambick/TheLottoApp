using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace TheLottoApp.Models
{
    public class NumberGeneratorViewModel
    {
        //[Required(ErrorMessage = "Required")]
        public int NumberOfOdds { get; set; }

        public int NumbersBelow15 { get; set; }

        public int NumbersBelow15And30 { get; set; }

        public int NumbersAbove30 { get; set; }

        public string ScoreRange { get; set; }

        public int NumbersOfPreviousRepeat { get; set; }

        public string NumbersToInclude { get; set; }

        public string NumbersToExclude { get; set; }

        public int NumberOfGames { get; set; }

        public int LottoId { get; set; }


        public int system { get; set; }

        public bool oddNumberForZero { get; set; }
        public bool oddNumberForOne { get; set; }
        public bool oddNumberForTwo { get; set; }
        public bool oddNumberForThree { get; set; }
        public bool oddNumberForFour { get; set; }
        public bool oddNumberForFive { get; set; }
        public bool oddNumberForSix { get; set; }
        public bool oddNumberForSeven { get; set; }
        public bool oddNumberForIgnore { get; set; }

        



    }
}