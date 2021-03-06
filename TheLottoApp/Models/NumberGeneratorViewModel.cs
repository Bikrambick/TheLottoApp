﻿using System;
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

        public int[] ScoreRange { get; set; }

        public int NumbersOfPreviousRepeat { get; set; }

        public int[] NumbersToInclude { get; set; }

        public int[] NumbersToExclude { get; set; }

        public int NumberOfGames { get; set; }


    }
}