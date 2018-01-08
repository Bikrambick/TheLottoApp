
    
class resul:
    def __init__(self, result):
        self.numbers = result
    
    
class get_the_statistics:
    def __init__(self,lottery_id,file_path):
        if lottery_id == 'ozlotto':
            with open(file_path) as file:
                self.results = []
                for line in file:
                    line=line.replace('\n','')
                    self.results.append(resul(','.join(line.split('\t'))))
            self.score_dict = {}
            count = 0
            for result in self.results:
                for ball in result.numbers.split(','):
                    count+=1
                    if ball in self.score_dict.keys():
                        self.score_dict[ball] +=1
                    else:
                        self.score_dict[ball] = 1 
    def get_numbers_statistict(self):
        numb_dict = {}
        for i in range(1,46):
            numb_dict[i] = self.score_dict[str(i)] 
        return numb_dict
    def get_prev_repeated(self):
        prev_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
        for i in range(len(self.results)-1):
            k = self.results[i].numbers.split(',')+self.results[i+1].numbers.split(',')
            total_repeated = len(k) - len(set(k))
            prev_dict[total_repeated] +=1
        for j in list(prev_dict):
            prev_dict[j] = round((prev_dict[j]/float(len(self.results)))*100,2)
        return prev_dict
    def get_nb_of_odds(self):
        odd_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
        for result in self.results:
            k = sum([int(x)%2==1 for x in result.numbers.split(',')])
            odd_dict[k] +=1
        for i in list(odd_dict):
            odd_dict[i] = round((odd_dict[i]/float(len(self.results)))*100,2)
        return odd_dict          
        
    def get_ranges(self):
        range_dict = {'Below 15':0, 'Between 15 and 30':0,'Above 30':0 }
        for result in self.results:
            k = sum([int(x)<15 for x in result.numbers.split(',')])
            range_dict['Below 15'] +=k
            l = sum([int(x)>=15 and int(x) <=30 for x in result.numbers.split(',')])
            range_dict['Between 15 and 30'] += l
            m = sum([int(x)>30 for x in result.numbers.split(',')])
            range_dict['Above 30'] += m
        for i in list(range_dict):
            range_dict[i] = round(range_dict[i]/float(len(self.results)),1) 
        return range_dict
        
    def get_score_chart(self):
        scores = []
        for result in self.results:
            tot_score = 0
            for ball in result.numbers.split(','):
                tot_score = tot_score + self.score_dict[ball]
            tot_score = tot_score / float(len(result.numbers.split(',')))
            tot_score = tot_score / float(len(self.results) * 7)
            scores.append(tot_score+0)
        scores.sort()
        return scores
    def get_time_score(self):
        scores = []
        for result in self.results:
            tot_score = 0
            for ball in result.numbers.split(','):
                tot_score = tot_score + self.score_dict[ball]
            tot_score = tot_score / float(len(result.numbers.split(',')))
            tot_score = tot_score / float((len(self.results) * 7))
            scores.append(tot_score+0)
        return scores

        