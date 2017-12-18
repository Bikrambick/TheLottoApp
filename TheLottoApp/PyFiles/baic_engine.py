### basic engine



import random
import math

    
class resul:
    def __init__(self, result):
        self.numbers = result
    
    
class get_the_basic_engine:
    def __init__(self):
        pass
    def get_set(self,lottery_id,strategy_id, nb_of_tickets_left, nb_of_games, system, user_plan, file_path):
        if nb_of_tickets_left < nb_of_games:
            return "You don't have enough tickets left, please, reduce number of games, upgrade the account or wait for balance update on Friday 6pm."
        if lottery_id == 'ozlotto':
            with open(file_path) as file:
                results = []
                for line in file:
                    line=line.replace('\n','')
                    results.append(resul(','.join(line.split('\t'))))
            ## retrieving results from the previous game
            maxresult = results[0]
            ######################################
            ## retrieving dictionary for score
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
            #########################################
            ## checking constraints for system:
            if system <7 or system > 20:
                return 'System number should be between 7 and 20'
            if user_plan != 'platinum' and system > 10:
                return 'If you want to generate system 10+, you need to upgrade to Platinum subscription'
            #########################################
            flag_for_middle = 0
            flag_for_nb_bigger_last = 0
            flag_for_nb_less_first = 0
            flag_for_odds = 0
            flag_for_prev_rep_num = 0
            flag_for_score_range = 0
            nb_bigger_last = 0
            nb_less_first = 0
            nb_middle = 0
            nb_of_odds =[3,4]
            nb_to_excl =''
            nb_to_inc =''
            prev_rep_numb = 0
            score_range = [0.018,0.026]
            
            #print(nb_less_first2, nb_middle2,nb_bigger_last2)
            if strategy_id == 'zero_prev_nb':
                flag_for_prev_rep_num = 1
                prev_rep_numb = 0
            elif strategy_id == 'balanced':
                flag_for_nb_less_first =1
                flag_for_middle = 1
                flag_for_nb_bigger_last = 1
                nb_bigger_last = 2
                nb_less_first = 2
                nb_middle = 3
                nb_less_first2 = []
                nb_middle2 = []
                nb_bigger_last2 = []
                X15 = nb_less_first * round((system-7)/7,1)
                X1530 = nb_middle * round((system-7)/7,1)
                X30 = nb_bigger_last * round((system-7)/7,1)
                nb_less_first2.append((nb_less_first+math.floor(X15))*flag_for_nb_less_first)
                nb_less_first2.append((nb_less_first+math.ceil(X15))*flag_for_nb_less_first)
                nb_middle2.append((nb_middle+math.floor(X1530))*flag_for_middle)
                nb_middle2.append((nb_middle+math.ceil(X1530))*flag_for_middle)
                nb_bigger_last2.append((nb_bigger_last+math.floor(X30))*flag_for_nb_bigger_last)
                nb_bigger_last2.append((nb_bigger_last+math.ceil(X30))*flag_for_nb_bigger_last)
                flag_for_odds = 1
                nb_of_odds = [3,4]
                nb_of_odds2 = []
                for num in nb_of_odds:
                    X = num * round((system-7)/7,1)
                    nb_of_odds2.append(num+math.floor(X))
                    nb_of_odds2.append(num+math.ceil(X))
                nb_of_odds2 = list(set(nb_of_odds2))
            elif strategy_id == 'best_score':
                flag_for_score_range = 1
                score_range = [0.020,0.0245]
            elif strategy_id == 'hot_numbers':
                ind = round(system/3)
                max_balls = []
                max_score = 0
                min_balls = []
                min_score = float('inf')
                for ball in list(score_dict):
                    if score_dict[str(ball)] >= max_score:
                        max_balls.append(ball)
                        max_score = score_dict[str(ball)]
                    if score_dict[str(ball)] <= min_score:
                        min_balls.append(ball)
                        min_score = score_dict[str(ball)]
                nb_to_inc = ','.join([str(x) for x in max_balls[-ind:]])
                nb_to_excl = ','.join([str(x) for x in min_balls[-ind:]])
                    
            ######################################
            ## generator
            max_iter = 500000
            generated_list = []
            for i in range(nb_of_games):
                counter = 0
                while True:
                    if len(nb_to_inc) >0:
                        List0 = [int(x) for x in nb_to_inc.split(',')]
                        List3 = random.sample([x for x in range(1,46) if str(x) not in List0+nb_to_excl.split(',')],system-len(List0))
                        if len(List0) + len(List3) == system:
                            List = List0+List3
                        else:
                            return 'generation error'
                    else:  
                        List = random.sample([x for x in range(1,46) if str(x) not in nb_to_excl.split(',')],system)
                    if flag_for_nb_less_first:
                        if sum([x<15 for x in List]) not in nb_less_first2:
                            counter +=1
                            if counter > max_iter:
                                return 'Too tight constraints', generated_list
                            continue
                    if flag_for_middle:
                        if sum([(x>=15 and x<=30) for x in List]) not in nb_middle2:
                            counter +=1
                            if counter > max_iter:
                                return 'Too tight constraints', generated_list
                            continue
                    if flag_for_nb_bigger_last:
                        if sum([x>30 for x in List]) not in nb_bigger_last2:
                            counter +=1
                            if counter > max_iter:
                                return 'Too tight constraints', generated_list
                            continue
                    if flag_for_odds:
                        if sum([x%2==1 for x in List]) not in nb_of_odds2:
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

