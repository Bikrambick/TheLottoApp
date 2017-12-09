import random

    
class resul:
    def __init__(self, result):
        self.numbers = result
    
    
class get_the_number:
    def __init__(self):
        pass
    def get_set(self,lottery_id,user_id,nb_of_odds, flag_for_odds, \
                                  nb_less_first, flag_for_nb_less_first, nb_middle, flag_for_middle, nb_bigger_last, flag_for_nb_bigger_last,\
                                  score_range, flag_for_score_range, prev_rep_numb, flag_for_prev_rep_num, \
                                  nb_to_inc, nb_to_excl, nb_of_games,file_path):
        if lottery_id == 'ozlotto':
            with open(file_path) as file:
                results = []
                for line in file:
                    line=line.replace('\n','')
                    results.append(resul(','.join(line.split('\t'))))
            ## retrieving results from the previous game
            if flag_for_prev_rep_num:
                if prev_rep_numb >7:
                    return 'Cannot return more than 7 numbers from previous game'
                maxresult = results[0]
                total_comb = 1
                left_balls = 45 - prev_rep_numb
                for num in range(7-prev_rep_numb):
                    total_comb = total_comb * left_balls
                    left_balls -=1
                if total_comb < nb_of_games:
                    return 'Too may constraints to generate '+str(nb_of_games) + ' games. \
                    Reduce number of balls from the previous game.'
            ######################################
            ## retrieving dictionary for score
            if flag_for_score_range:
                setscore = 0
                score_dict = {}
                count = 0
                for result in results:
                    for ball in result.numbers.split(','):
                        count+=1
                        if ball in score_dict.keys():
                            score_dict[ball] +=1
                        else:
                            score_dict[ball] = 1 
            ########################################
            ## checking constraints for score
            if score_range[-1] - score_range[0] < (0.001):
                return 'Too narrow score range: increase it or drop the filter for score range.'
            if score_range[-1] < 0.0220  and nb_of_games > 20:
                return 'The top range marker is set too low for this number of games, please,\
                increase the interval or decrease the number of games to below 20.'
                
            #########################################
            ## checking constraints for include and exclude
            if len(nb_to_inc) > 0:
                if len(nb_to_inc.split(',')) >7:
                    return 'Cannot include more than 7 numbers'
                if len(nb_to_inc.split(',')) == 7:
                    return 'You cannot predefine 7 numbers, that is only one combination'
                total_comb = 1
                left_balls = 45 - len(nb_to_inc.split(','))
                for num in range(7-len(nb_to_inc.split(','))):
                    total_comb = total_comb * left_balls
                    left_balls -=1
                for num in nb_to_inc.split(','):
                    if int(num) >45 or int(num) <1:
                        return 'You can only include numbers between 1 and 45'
                if total_comb < nb_of_games:
                    return 'Too may constraints to generate '+str(nb_of_games) + ' games. \
                    Eliminate some numbers from field "numbers to include"'
            if len(nb_to_excl) > 0:
                if len(nb_to_inc.split(',')) > 45-7:
                    return 'Too many numbers to exclude'
                if len(nb_to_inc.split(',')) == 45-7:
                    return 'You cannot exclude all numbers apart from 7, that is only one combination'
                total_comb = 1
                for num in range(45-len(nb_to_excl.split(',')),45-len(nb_to_excl.split(','))-7,-1):
                    total_comb = total_comb * num
                if total_comb < nb_of_games:
                    return 'Too may constraints to generate '+str(nb_of_games) + ' games. \
                    Eliminate some numbers from field "numbers to exclude"'
            if len(nb_to_excl) > 0 and len(nb_to_inc) >0:
                for numb in nb_to_inc.split(','):
                    if numb in nb_to_excl.split(','):
                        return 'You cannot include and exclude number '+str(numb)+' at the same time'
            ###########################################
            ## check constrtaints for odd requirements
            if flag_for_odds:
                if nb_of_odds >7:
                    return 'You are requiring too many odds'
                if flag_for_prev_rep_num:
                 #   print('Previous game: ',maxresult.numbers.split(','))
                    all_n =  [int(x)%2==1 for x in maxresult.numbers.split(',')]
                    if (7 - prev_rep_numb + min(sum(all_n), prev_rep_numb)) < nb_of_odds:
                              return 'Not enough odd numbers in previous game or \
                              you are requiring too many odds'
                    if prev_rep_numb - sum([int(x)%2==0 for x in maxresult.numbers.split(',')]) > nb_of_odds:
                        return 'Now enough even numbers in previous game'
                if len(nb_to_inc) > 0:
                    if 7 - len(nb_to_inc.split(',')) + sum([int(x)%2==1 for x in nb_to_inc.split(',')]) < nb_of_odds:
                        return 'Not enough odd numbers in numbers required to include'
                    if sum([int(x)%2==1 for x in nb_to_inc.split(',')]) > nb_of_odds:
                        return 'Too many odd numbers in numbers required to include'
                if len(nb_to_excl) > 0:
                    if 23 - sum([int(x)%2==1 for x in nb_to_excl.split(',')]) < nb_of_odds:
                        return 'Too many odd numbers eliminated'
                    if 22-sum([int(x)%2==0 for x in nb_to_excl.split(',')]) < 7-nb_of_odds:
                        return 'Too many even numbers eliminated'
            ######################################
            ## check constraitns for lower first
            if flag_for_nb_less_first:
                if nb_less_first >7:
                    return 'You are requiring too many numbers to be less than 15'
                if flag_for_nb_bigger_last:
                    if 7-nb_less_first < nb_bigger_last:
                        return 'Check the requirements for "below 15", seems like it \
                        contradict the requirement for "above 30". '
                if flag_for_middle:
                    if 7-nb_less_first < nb_middle:
                        return 'Check the requirements for "below 15", seems like it \
                        contradict the requirement for "between 15 and 30". '
                if flag_for_prev_rep_num:
                    if 7 - prev_rep_numb + min(sum([int(x)<=15  for x in maxresult.numbers.split(',')]),prev_rep_numb) < nb_less_first:
                              return 'Not enough numbers below 15 in previous game or \
                              you are requiring too many numbers to be below 15'
                    if prev_rep_numb - sum([int(x)>15 for x in maxresult.numbers.split(',')]) > nb_less_first:
                        return 'Now enough numbers above 15 in the previous game'
                if len(nb_to_inc) > 0:
                    if 7 - len(nb_to_inc.split(',')) + sum([int(x)<=15 for x in nb_to_inc.split(',')]) < nb_less_first:
                        return 'Not enough numbers below 15 in numbers required to include'
                    if sum([int(x)<=15 for x in nb_to_inc.split(',')]) > nb_less_first:
                        return 'Too many numbers below 15 in numbers required to include'
                if len(nb_to_excl) > 0:
                    if 15 - sum([int(x) <= 15 for x in nb_to_excl.split(',')]) < nb_less_first:
                        return 'Too many numbers below 15 eliminated'
                    if 30-sum([int(x)>15 for x in nb_to_excl.split(',')]) < 7-nb_less_first:
                        return 'Too many numbers above 15 are eliminated'
            ######################################
            ## check constraitns for in the middle
            if flag_for_middle:
                if flag_for_middle and flag_for_nb_bigger_last and flag_for_nb_less_first:
                    if nb_bigger_last+nb_less_first + nb_middle != 7:
                        return 'Requirements for numbers before 15, between 15 and 30 and above 30 should sum up to 7'
                if nb_middle >7:
                    return 'You are requiring too many numbers to be between 15 and 30'
                if flag_for_nb_less_first:
                    if 7-nb_middle < nb_less_first:
                        return 'Check the requirements for "between 15 and 30", seems like it \
                        contradict the requirement for "less than 15". '
                if flag_for_nb_bigger_last:
                    if 7-nb_middle < nb_bigger_last:
                        return 'Check the requirements for "between 15 and 30", seems like it \
                        contradict the requirement for "above 30". '
                if flag_for_prev_rep_num:
                    if 7 - prev_rep_numb + min(sum([(int(x)>15) and (int(x)<30) for x in maxresult.numbers.split(',')]),prev_rep_numb) < nb_middle:
                              return 'Not enough numbers between 15 and 30 in previous game or \
                              you are requiring too many numbers to be between 15 and 30'
                    if prev_rep_numb - sum([(int(x)<=15)or(int(x)>=30) for x in maxresult.numbers.split(',')]) > nb_middle:
                        return 'Now enough numbers below 15 and above 30 in the previous game'
                if len(nb_to_inc) > 0:
                    if 7 - len(nb_to_inc.split(',')) + sum([(int(x)>15) and (int(x)<30) for x in nb_to_inc.split(',')]) < nb_middle:
                        return 'Not enough numbers between 15 and 30 in numbers required to include'
                    if sum([(int(x)>15) and (int(x)<30) for x in nb_to_inc.split(',')]) > nb_middle:
                        return 'Too many numbers between 15 and 30 in numbers required to include'
                if len(nb_to_excl) > 0:
                    if 15 - sum([(int(x)>15) and (int(x)<30) for x in nb_to_excl.split(',')]) < nb_middle:
                        return 'Too many numbers between 15 and 30 eliminated'
                    if 30-sum([(int(x)<=15)or(int(x)>=30) for x in nb_to_excl.split(',')]) < 7-nb_middle:
                        return 'Too many numbers bellow 15 and above 30 are eliminated'
            ######################################
            ## check constraitns for bigger last
            if flag_for_nb_bigger_last:
                if nb_bigger_last >7:
                    return 'You are requiring too many numbers to be above 30'
                if flag_for_nb_less_first:
                    if 7-nb_bigger_last < nb_less_first:
                        return 'Check the requirements for "above 30", seems like it \
                        contradict the requirement for "below 15". '
                if flag_for_middle:
                    if 7-nb_bigger_last < nb_middle:
                        return 'Check the requirements for "above 30", seems like it \
                        contradict the requirement for "between 15 and 30". '
                if flag_for_prev_rep_num:
                    if 7 - prev_rep_numb + min(sum([int(x)>=30  for x in maxresult.numbers.split(',')]),prev_rep_numb) < nb_bigger_last:
                              return 'Not enough numbers above 30 in previous game or \
                              you are requiring too many numbers to be above 30'
                    if prev_rep_numb - sum([int(x)<30 for x in maxresult.numbers.split(',')]) > nb_bigger_last:
                        return 'Now enough numbers below 30 in the previous game'
                if len(nb_to_inc) > 0:
                    if 7 - len(nb_to_inc.split(',')) + sum([int(x)>=30 for x in nb_to_inc.split(',')]) < nb_bigger_last:
                        return 'Not enough numbers above 30 in numbers required to include'
                    if sum([int(x)>=30 for x in nb_to_inc.split(',')]) > nb_bigger_last:
                        return 'Too many numbers above 30 in numbers required to include'
                if len(nb_to_excl) > 0:
                    if 15 - sum([int(x) >= 30 for x in nb_to_excl.split(',')]) < nb_bigger_last:
                        return 'Too many numbers above 30 eliminated'
                    if 30-sum([int(x)<30 for x in nb_to_excl.split(',')]) < 7-nb_bigger_last:
                        return 'Too many numbers below 30 are eliminated'
            ######################################
            ## check constraitns for nb_to_include and previous
            if flag_for_prev_rep_num and len(nb_to_inc.split(',')) >0:
                if 7 - len(nb_to_inc.split(',')) +sum([x in maxresult.numbers.split(',') \
                           for x in nb_to_inc.split(',')]) < prev_rep_numb:
                    return 'Not enough numbers required to include in previous game'
            ## check constraints for nb_to_exclude and previous
            if flag_for_prev_rep_num and len(nb_to_excl.split(',')) > 0:
                if 7 - sum([x in nb_to_excl.split(',') for x in maxresult.numbers.split(',')]) < prev_rep_numb:
                    return 'Not enough numbers left in previous game after eliminating the ones to exclude'    
            ## check constraint for number of games
            if nb_of_games > 500:
                return 'Too many games to generate'
                    
            ######################################
            ## generator
            max_iter = 300000
            generated_list = []
            #print(maxresult.numbers.split(','))
            for i in range(nb_of_games):
                counter = 0
                while True:
                    if flag_for_prev_rep_num:
                        List1 = random.sample([int(y) for y in maxresult.numbers.split(',')],prev_rep_numb)
                        List2 = random.sample([x for x in range(1,46) if x not in List1],7-prev_rep_numb)
                        if len(List1) + len(List2) ==7:
                            List = List1 + List2
                        else:
                            return 'wrong list concaenationt'
                    else:
                        List = random.sample(range(1,46),7)
                    if flag_for_nb_less_first:
                        if sum([x<=15 for x in List]) !=nb_less_first:
                            counter +=1
                            if counter > max_iter:
                                return 'Too tight constraints', generated_list
                            continue
                    if flag_for_middle:
                        if sum([(x>=15 and x<=30) for x in List]) !=nb_middle:
                            counter +=1
                            if counter > max_iter:
                                return 'Too tight constraints', generated_list
                            continue
                    if flag_for_nb_bigger_last:
                        if sum([x>=30 for x in List]) != nb_bigger_last:
                            counter +=1
                            if counter > max_iter:
                                return 'Too tight constraints', generated_list
                            continue
                    if flag_for_odds:
                        if sum([x%2==1 for x in List]) != nb_of_odds:
                            counter +=1
                            if counter > max_iter:
                                return 'Too tight constraints', generated_list
                            continue
                    if flag_for_prev_rep_num:
                        if sum([x in [int(y) for y in maxresult.numbers.split(',')] for x in List]) != prev_rep_numb:
                            counter +=1
                            if counter > max_iter:
                                return 'Too tight constraints', generated_list
                            continue
                    if len(nb_to_inc)>0:
                        if sum([str(x) in nb_to_inc.split(',') for x in List]) != len(nb_to_inc.split(',')):
                            counter +=1
                            if counter > max_iter:
                                return 'Too tight constraints', generated_list
                            continue
                    if len(nb_to_excl)>0:
                        if sum([str(x) in nb_to_excl.split(',') for x in List]) != 0:
                            counter +=1
                            if counter > max_iter:
                                return 'Too tight constraints', generated_list
                            continue
                    if flag_for_score_range:
                        for ball in List:
                            setscore = setscore + score_dict[str(ball)]
                        setscore = setscore / len(List)
                        setscore= setscore/count
                        #print(setscore)
                        if setscore > score_range[-1] or sum(List) < score_range[0]:
                            counter +=1
                            if counter > max_iter:
                                return 'Too tight constraints', generated_list
                            continue
                    List=sorted(List)
                    if List not in generated_list:
                        generated_list.append(List)  
                        break
                    else:
                        counter +=1
                        if counter > max_iter:
                            return 'Too tight constraints', generated_list
                        continue
            return generated_list


