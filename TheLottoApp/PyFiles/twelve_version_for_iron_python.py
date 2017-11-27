import math
from math import sqrt
#from random import randint
#from scipy.stats import norm
#from dateutil import parser
from datetime import datetime
#import random


class cust_constant:
    def __init__(self,  cur_age, contribution, Current_super_acct_balance, \
                 Expected_retirement_age, Additional_contribution , Homeowner ,married,\
                 Value_of_home, Downsize_home_at_age, PVR):
        self.Percentage_Value_released = PVR/100.0
        self.current_date = datetime.now()
        self.Homeowner = Homeowner
        self.Value_of_home = Value_of_home
        self.home_value = self.Value_of_home*self.Percentage_Value_released
        self.Current_super_acct_balance = Current_super_acct_balance
        self.cur_age = cur_age
        self.married = married
        self.current_salary = contribution/(1-constants.cc_tax_rate)/constants.SCG_list[self.current_date.year-2000]
        self.Downsize_home_at_age = Downsize_home_at_age
        self.Expected_retirement_age = Expected_retirement_age
        self.Additional_contribution = Additional_contribution/100.0
#        self.AA_customer = [AA_Equity/100.0,AA_Bond/100.0,AA_Cash/100.0,AA_Property/100.0,AA_OS_Eq/100.0]#hundreds
        self.month = self.current_date.month
        self.CFT = constants.CFT[self.month]
        self.Asset_test_level = (450 -(Homeowner*200)+(married*125))*1000
        self.Pension_Amount = 22805-(married*5614)

##input from customer 16 variables:###################################################
def parse_customer_data(cur_age, contribution, Current_super_acct_balance, \
                 Expected_retirement_age, Additional_contribution ,Homeowner ,married,\
                 Value_of_home = 1000000, Downsize_home_at_age = 80 , PVR = 30):    
    global cust_constants
    cust_constants = cust_constant(cur_age, contribution, Current_super_acct_balance, \
                 Expected_retirement_age, Additional_contribution , Homeowner ,married,\
                 Value_of_home, Downsize_home_at_age, PVR)


class constant:
    def __init__(self, Real_salary_growth, taper_rate,\
                 Fee_fixed_work, Fee_perc_work, \
                 Fee_fix_retired, Fee_perc_retired,AWE_list, SCG_list, cc_tax_rate,\
                 WD_list,CFT,Pen_list,Tax_non_sup,top_max_age,norms,FV,ERR,Types_of_AA,AA_input,Expected_age):
        self.Real_salary_growth = 1+(Real_salary_growth/100.0)
        self.Taper_rate = taper_rate*0.026089285714285714
        self.Fee_fixed_work = Fee_fixed_work 
        self.Fee_perc_work = Fee_perc_work/100.0
        self.Fee_fix_retired = Fee_fix_retired
        self.Fee_perc_retired = Fee_perc_retired/100.0
        self.AWE_list = AWE_list
        self.SCG_list = SCG_list
        self.cc_tax_rate = cc_tax_rate/100.0
        self.WD_list = WD_list
        self.Pen_list = Pen_list
        self.Tax_non_sup = 1-(Tax_non_sup/100.0)
        self.top_max_age = top_max_age
        self.norms = norms
        self.FV = FV
        self.ERR = ERR
        self.Types_of_AA = Types_of_AA
        self.AA_input = AA_input
        self.Expected_age = Expected_age
        self.CFT = CFT
        
#Input from administrator:#############################################
def parse_admin_data(path_to_server, max_age = 100,nb_of_iter = 1000,Expected_age = 90 ,\
                     Account_fees_FIXED_when_working =100, Account_fees_Ad_Valorem_when_working=0.5,\
                     Account_fees_FIXED_in_retirement=100, Account_fees_Ad_Valorem_in_retirement = 0.5,\
                     CFT = {1:1,2:1,3:1,4:0.5,5:0.5,6:0.5,7:0.5,8:0.5,9:0,10:0,11:0,12:0} ,\
                           cc_tax_rate =15, Real_salary_growth = 0.5,  seed_for_random = 5, \
                           Taper_rate = 3,Tax_non_sup = 25):
    global constants
    top_max_age = max_age+1
    AWE_list = [0 for x in range(0,top_max_age)]
    SCG_list = [0 for x in range(0,top_max_age)]
    WD_list = [1 for x in range(0,top_max_age)]
    AA_input = {}
    #create_random_numbers(max_age,seed_for_random,nb_of_iter) 
    Pen_list = [0 for x in range(0,top_max_age)]
    with open(path_to_server+'AWE.txt') as file:
        for line in file:
            line = line.split('\t')
            AWE_list[int(line[0])] = int(line[1].replace('\n',''))
    with open(path_to_server+'SCG_rate.txt') as file:
        for line in file:
            line = line.split('\t')
            SCG_list[int(line[0])] = float(line[1].replace('\n','').replace(',','.'))/100.0
    with open(path_to_server+'AA.txt') as file:
        for line in file:
            if line[0] == '#':
                continue
            line = line.split('\t')
            line[5] = line[5].replace('\n','')
            AA_input[line[0]] = [int(x)/100.0 for x in line[1:6]]
    Types_of_AA = list(AA_input)    
    with open(path_to_server+'WDprofile.txt') as file:
        for line in file:
            line = line.split('\t')
            WD_list[int(line[0])] = float(int(line[1].replace('\n',''))/100.0 )
                   
    with open(path_to_server+'Pen_perc.txt') as file:
        for line in file:
            line = line.split('\t')
            Pen_list[int(line[0])] = int(line[1].replace('\n',''))/100.0
    norms = [0 for x in range(0,nb_of_iter)]
    with open(path_to_server+'randoms.txt') as file:
        counter = 0
        for line in file:
            line = line.replace('\n','')
            line = line.split(' ')
            norms[counter] = [float(x) for x in line if x !='']
            counter+=1
            if counter >= nb_of_iter:
                break
    #Estimated real return s
    ERR_Equity = 7 #%
    ERR_Bond	= 3#%
    ERR_Cash	= 1#%
    ERR_Property	= 7#%
    ERR_OS_Eq =7#%
    #Future Volatility
    FV_Equity = 20 #%
    FV_Bond	= 4#%
    FV_Cash	= 1#%
    FV_Property	= 15#%
    FV_OS_Eq =20#%
    FV = [FV_Equity/100.0,FV_Bond/100.0,FV_Cash/100.0,FV_Property/100.0,FV_OS_Eq/100.0] # hundreds
    ERR = [ERR_Equity/100.0,ERR_Bond/100.0,ERR_Cash/100.0,ERR_Property/100.0,ERR_OS_Eq/100.0] # hundreds
    constants = constant(Real_salary_growth,Taper_rate,\
                  Account_fees_FIXED_when_working, \
                  Account_fees_Ad_Valorem_when_working, Account_fees_FIXED_in_retirement, \
                  Account_fees_Ad_Valorem_in_retirement, AWE_list, SCG_list, cc_tax_rate,\
                  WD_list, CFT,Pen_list,Tax_non_sup,top_max_age,norms,FV,ERR,Types_of_AA,AA_input,Expected_age)    

#def create_random_numbers(max_age, seed1,nb_of_iter):
#    with open('randoms.txt', 'w') as texfile:
#        random.seed(seed1)
#        for i in range(0,nb_of_iter):
#            inc_random = random.uniform(0.00000000000001,0.99999999999999)
#            print(norm.ppf(inc_random),' ',sep = '',end = '',file = texfile)
#            for j in range(19,max_age+1):
#                if j %2 ==1:
#                    inc_random = 1-inc_random
#                else:
#                    inc_random = random.uniform(0.00000000000001,0.99999999999999)
#                print(norm.ppf(inc_random),' ',sep = '',end = '',file = texfile)
#            print('',file = texfile)
 
# all the data about customer by age, independent on type of allocation                  
class aging:
    def __init__(self,age,home_downsize_age,Expected_retirement_age,Age_list, add_contr):
        global constants
        global cust_constants
        self.age = age
        if age == cust_constants.cur_age:
            self.salary = cust_constants.current_salary
        else:
            age_factor = constants.AWE_list[age]/(constants.AWE_list[cust_constants.cur_age]*1.0)
            self.salary = round((cust_constants.current_salary)*age_factor*((constants.Real_salary_growth)**(age-cust_constants.cur_age)),2)
        if age >= Expected_retirement_age:
            self.retired = True
            self.fixed_fee = constants.Fee_fix_retired
            self.perc_fee = constants.Fee_perc_retired
            self.net_contribution = 0
            self.WD_profile = constants.WD_list[age]
            self.WDW_perc = constants.Pen_list[age]
            self.Pension_Amount = cust_constants.Pension_Amount
        else:
            self.retired = False
            self.fixed_fee = constants.Fee_fixed_work
            self.perc_fee = constants.Fee_perc_work
            self.net_contribution = round((1-\
                                     (constants.cc_tax_rate))*(self.salary*\
                                     constants.SCG_list[cust_constants.current_date.year+(age-cust_constants.cur_age)-2000]),2) \
                                     + round(add_contr*self.salary,2)
            self.WD_profile = 0
            self.WDW_perc = 0
            self.Pension_Amount = 0
        if home_downsize_age == age and cust_constants.Homeowner:
            self.home_downsize_age = True
        else:
            self.home_downsize_age = False
        if age == home_downsize_age:
            if cust_constants.Homeowner: 
                self.Assets_Inflow = cust_constants.home_value
            else:
                self.Assets_Inflow = 0
        else:
            self.Assets_Inflow = 0   


class Allocation:
    def __init__(self, A_type, AA,FV,ERR):
        self.A_type = A_type
        self.E_return= sum([AA[x]*ERR[y] for x in range(0,len(AA)) for y in range(0,len(ERR)) if x==y])
        self.Volatility =sqrt(sum([(AA[x]**2)*(FV[y]**2) for x in range(0,len(AA)) for y in range(0,len(FV)) if x==y]))
        self.LP_ST_dev= sqrt(math.log(1+((self.Volatility**2)/float(((1+self.E_return)**2)))))
        self.LP_Mean=math.log(1+self.E_return) - ((self.LP_ST_dev)**2)/2.0



class cashflow:
    def __init__(self, age,AAl_type,Age_list,Desired_income,use_random,itera,constants,cust_constants):
        self.start_period = cust_constants.Current_super_acct_balance
        self.Start_asset_period = 0
        if use_random == 1:
            self.Investment_return = math.e**(AAl[AAl_type].LP_Mean+AAl[AAl_type].LP_ST_dev*constants.norms[itera][age-18])
        else:
            self.Investment_return=math.e**(AAl[AAl_type].LP_Mean)
        taxnonsup = self.Investment_return*(constants.Tax_non_sup)
        Main_Wdw = Age_list[age].WDW_perc*self.start_period
        trashold = self.start_period + self.Start_asset_period
        if ((trashold) > cust_constants.Asset_test_level) and Age_list[age].retired:
            self.Pension = max(0,Age_list[age].Pension_Amount - constants.Taper_rate*(trashold - cust_constants.Asset_test_level))
        else:
            self.Pension =   Age_list[age].Pension_Amount 
        if cust_constants.married:
            self.Pension = self.Pension*2
        self.Assets_Outflow = max(0,min(self.Start_asset_period + \
                                  Age_list[age].Assets_Inflow,(Desired_income*\
                                          Age_list[age].WD_profile)-self.Pension-Main_Wdw))
        total_fee = min(max(0,self.start_period - \
                                 Age_list[age].fixed_fee),self.start_period * \
        Age_list[age].perc_fee+Age_list[age].fixed_fee)
        self.end_asset_period = self.Start_asset_period  * taxnonsup +\
                                Age_list[age].Assets_Inflow -  self.Assets_Outflow*taxnonsup *min(1,max(cust_constants.CFT,0))  
        net_start_period = self.start_period - total_fee
        self.add_WDW = max(0,min(Desired_income*Age_list[age].WD_profile - Main_Wdw - \
                           self.Assets_Outflow - self.Pension, net_start_period - Main_Wdw)    )              
        self.Total_WDW = min(self.add_WDW + Main_Wdw,net_start_period)
        cashflow = max(-self.start_period,Age_list[age].net_contribution-total_fee-self.Total_WDW)                  
        if cashflow >0:
            self.end_period = (self.start_period *self.Investment_return + \
                               cashflow * self.Investment_return*min(1,max(cust_constants.CFT,0)))
        else:
            self.end_period = (self.start_period *self.Investment_return + \
                               cashflow)
   
    def update(self,age,AAl_type,Age_list,Desired_income,use_random,itera,constants,cust_constants):
        self.start_period = self.end_period
        self.Start_asset_period = self.end_asset_period 
        if use_random == 1:
            self.Investment_return = math.e**(AAl[AAl_type].LP_Mean+AAl[AAl_type].LP_ST_dev*constants.norms[itera][age-18])
        else:
            self.Investment_return = math.e**(AAl[AAl_type].LP_Mean)
        taxnonsup = self.Investment_return*constants.Tax_non_sup
        Main_Wdw = Age_list[age].WDW_perc*self.start_period
        trashold = self.start_period + self.Start_asset_period
        if (trashold > cust_constants.Asset_test_level) and Age_list[age].retired:
            self.Pension = max(0,Age_list[age].Pension_Amount - constants.Taper_rate*(trashold - cust_constants.Asset_test_level))
        else:
            self.Pension =   Age_list[age].Pension_Amount 
        if cust_constants.married:
            self.Pension = self.Pension*2
        self.Assets_Outflow = max(0,min(self.Start_asset_period + \
                                  Age_list[age].Assets_Inflow,Desired_income*\
                                          Age_list[age].WD_profile-self.Pension-Main_Wdw))
        total_fee = min(max(0,self.start_period - \
                                 Age_list[age].fixed_fee),self.start_period * \
        Age_list[age].perc_fee+Age_list[age].fixed_fee)
        self.end_asset_period = self.Start_asset_period  * taxnonsup +  Age_list[age].Assets_Inflow -  self.Assets_Outflow*(taxnonsup *min(1,max(cust_constants.CFT,0)))  
        net_start_period = self.start_period - total_fee
        self.add_WDW = max(0,min(Desired_income*Age_list[age].WD_profile- Main_Wdw - \
                           self.Assets_Outflow - self.Pension, net_start_period - Main_Wdw)    )              
        self.Total_WDW = min(self.add_WDW + Main_Wdw,net_start_period)
        cashflow = max(-self.start_period,Age_list[age].net_contribution-total_fee-self.Total_WDW)                  
        if cashflow >0:
            self.end_period = (self.start_period *self.Investment_return + \
                               cashflow * self.Investment_return*min(1,max(cust_constants.CFT,0)))
        else:
            self.end_period = (self.start_period *self.Investment_return + \
                               cashflow) 




############## Allocation calculating ########################
def Allocation_calculations():
    global constants
    global cust_constants
    global AAl
#    constants.Types_of_AA = constants.Types_of_AA +['Customer']
#    constants.AA_input['Customer'] = cust_constants.AA_customer
    AAl = {}
    for i in constants.Types_of_AA:
        AAl[i] = Allocation(i,constants.AA_input[i],constants.FV,constants.ERR)
##############################################################

############# Aging function #################################

def create_aging(cur_age, downsize_home, top_max_age,Expected_retirement_age, add_contr):
    global Age_list
    Age_list = [x for x in range(0,top_max_age)]
    for i in range(cur_age,top_max_age): 
        Age_list[i]=aging(i, downsize_home, Expected_retirement_age,Age_list,add_contr)
############## Annual Incomes calculation ####################
############## 0.07 seconds
def Annual_income_calc():
    global EI_dict
    global Age_list
    global AAl
    global constants
    global cust_constants
    Years_to_live = constants.Expected_age +5 - cust_constants.Expected_retirement_age
    EI_dict = {}
    for t in constants.Types_of_AA:
        Cur_value= cust_constants.Current_super_acct_balance*((1+AAl[t].E_return)**(cust_constants.Expected_retirement_age \
                  - cust_constants.cur_age ))
        Contrib = Age_list[cust_constants.cur_age].net_contribution*(constants.Real_salary_growth**(cust_constants.Expected_retirement_age \
                  - cust_constants.cur_age )) \
                  *((1 + AAl[t].E_return)**(cust_constants.Expected_retirement_age \
                  - cust_constants.cur_age )) * (cust_constants.Expected_retirement_age- cust_constants.cur_age)/4.0
        if cust_constants.married:
            Pension = cust_constants.Pension_Amount * Years_to_live *2
        else:
            Pension = cust_constants.Pension_Amount * Years_to_live
        if cust_constants.Homeowner:
            House_amount = (cust_constants.Value_of_home * cust_constants.Percentage_Value_released)\
                       *(1+AAl[t].E_return)**(constants.Expected_age-5-cust_constants.Downsize_home_at_age)
        else:
            House_amount = 0
        EI_dict[t] = [((Cur_value+Contrib+Pension+House_amount)//Years_to_live)*(4.0/5.0)]
    for t in list(EI_dict):
        EI_dict[t][0] =  int(EI_dict[t][0] - EI_dict[t][0] % 1000 - 1000)
#        step = (EI_dict[t][0] / 12.0 - (EI_dict[t][0] / 12.0)%1000) +4000
        step = ((EI_dict[t][0]*5/12.0) - (EI_dict[t][0]*5/12.0) % 1000)    
        for _ in range(0,6):
            EI_dict[t].append(int(EI_dict[t][-1]+step))
##############################################################


############## Calculating 100 iters for respective annual income for running out age
def calc_resp_ann_income():
    global Age_list
    global EI_dict
    global ret_inc_run_at_age
    global constants
    global cust_constants
    global new_ret_inc
    ret_inc_run_at_age = {}
    new_ret_inc = {}
    for al in constants.Types_of_AA:
        new_ret_inc[al] = {}
        ret_inc_run_at_age[al] = {}
        for i in list(EI_dict[al]):
            list_of_lifes = []
#            create_aging(cust_constants.cur_age,cust_constants.Downsize_home_at_age,constants.top_max_age,cust_constants.Expected_retirement_age)
#            house_sold = 0
            for k in range(1,100):
                CFinstance = cashflow(cust_constants.cur_age,al,Age_list,i,1,k,constants,cust_constants)
                j = cust_constants.cur_age+1
#                house_sold = 0
                flag = 0
                while j < constants.top_max_age-1: 
                    CFinstance.update(j,al,Age_list,i,1,k,constants,cust_constants)
#                    if Age_list[j].home_downsize_age and house_sold == 0:
#                        house_sold = 1
#                    if j >= cust_constants.Expected_retirement_age:
#                        if house_sold == 0:
#                            if CFinstance.end_period < i *1.5:
#                                create_aging(cust_constants.cur_age,j+1,constants.top_max_age,cust_constants.Expected_retirement_age)
#                                house_sold = 1
                    if j>=65 and CFinstance.end_period < i:# and house_sold == 1:
                        list_of_lifes.append(j)
                        flag = 1
                        break
                    j+=1
                if flag == 0:
                    list_of_lifes.append(j-1)
#            print(al, sorted(list_of_lifes))
            a = sorted(list_of_lifes)
            ret_inc_run_at_age[al][i] = []
            procentiles = [85,66,50,33,15]
            for p in procentiles:
                ret_inc_run_at_age[al][i].append([p,int(a[p])])
        for procen in [0,1,2,3,4]:
            new_ret_inc[al][procen] = []
            for alloc in list(EI_dict[al]):
                new_ret_inc[al][procen].append(ret_inc_run_at_age[al][alloc][procen][1]) 
#            a = np.array(list_of_lifes)
#            ret_inc_run_at_age[al][i] = []
#            procentiles = [85,66,50,33,15]
#            for p in range(len(procentiles)) :
#                ret_inc_run_at_age[al][i].append([procentiles[p],int(np.percentile(a,procentiles[p],interpolation = 'linear'))]) 


#############################################################

############# Calculating income with survival by 90 ########
def calc_income_by_90():
    global ret_inc_run_at_age
    global EI_dict
    global Income_by_90
    global constants
    global cust_constants
    Income_by_90 = {}
    for al in constants.Types_of_AA:
        past_inc = 0
        past_age = 90
        for i in range(len(list(EI_dict[al]))):
            if ret_inc_run_at_age[al][EI_dict[al][i]][1][1] >= 90:
                past_inc = EI_dict[al][i]
                past_age = ret_inc_run_at_age[al][EI_dict[al][i]][1][1]
            else: 
                if past_inc > 0:
                    Income_by_90[al] = int((EI_dict[al][i]-(90 - ret_inc_run_at_age[al][EI_dict[al][i]][1][1])*((EI_dict[al][i] - \
                                past_inc)/float((past_age-ret_inc_run_at_age[al][EI_dict[al][i]][1][1])))//100 *100))
                    break
                else:
                    Income_by_90[al] = int(EI_dict[al][0]*(ret_inc_run_at_age[al][EI_dict[al][0]][1][1]-(90-ret_inc_run_at_age[al][EI_dict[al][0]][1][1]))/float(ret_inc_run_at_age[al][EI_dict[al][0]][1][1]))
                    break
        if al not in list(Income_by_90):
            Income_by_90[al] = int(EI_dict[al][-1]*(past_age-90+past_age)/float(past_age))
    return Income_by_90
    
#############################################################
        

############## calculating assets and cashflow ##########################
def calc_assets():
    global assets_probab
    global constants
    global cust_constants
    assets_probab = {}
    for t in constants.Types_of_AA:
        assets_probab[t] = {}
        SP_assets_list = [ [] for x in range(0,101)]
        for k in range(0,100):
            CFinstance = cashflow(cust_constants.cur_age,t,Age_list,Income_by_90[t],1,k,constants,cust_constants)
            i=50
            if i == cust_constants.cur_age:
                SP_assets_list[i].append(CFinstance.start_period)
            j = cust_constants.cur_age +1
            while i < constants.top_max_age:
                while j <i:
                    CFinstance.update(j,t,Age_list,Income_by_90[t],1,k,constants,cust_constants)
                    j+=1
                SP_assets_list[i].append(CFinstance.start_period)
                i+=5
        for p in [85,66,50,33,15]:
            assets_probab[t][p] = []
            for j in SP_assets_list:
                if j == []:
                    continue
                a = sorted(j)
                assets_probab[t][p].append(int(a[p]))
#                a = np.array(j)
#                assets_probab[t][p].append(int(np.percentile(a,p,interpolation = 'linear')))
    return assets_probab



def calculate_cashflow():
    global Cash_flow
    global Age_list
    global Income_by_90
    global constants
    global cust_constants
    Cash_flow = {}
    #Cash_flow['Describe'] = 'Age, Super Withdrowals, Pension, Other Assets'
    for t in constants.Types_of_AA:
        Cash_flow[t] = []        
        CFinstance = cashflow(cust_constants.cur_age,t,Age_list,Income_by_90[t],0,0,constants,cust_constants)
        j=cust_constants.cur_age+1
        house_sold = 0
        create_aging(cust_constants.cur_age,cust_constants.Downsize_home_at_age,constants.top_max_age,cust_constants.Expected_retirement_age,cust_constants.Additional_contribution)
        counter = 0
        while j < constants.top_max_age:
            CFinstance.update(j,t,Age_list,Income_by_90[t],0,0,constants,cust_constants) 
            if Age_list[j].home_downsize_age and house_sold == 0:
                house_sold = 1
            if j >= cust_constants.Expected_retirement_age:
                if house_sold == 0:
                    if CFinstance.end_period < Income_by_90[t] *1.5:
                        create_aging(cust_constants.cur_age,j+1,constants.top_max_age,cust_constants.Expected_retirement_age,cust_constants.Additional_contribution)
                        house_sold = 1
                Cash_flow[t].append([j])
                Cash_flow[t][counter].append([int(CFinstance.Total_WDW),int(CFinstance.Pension),int(CFinstance.Assets_Outflow)])
                counter +=1
            j+=1  
    return Cash_flow    

def calculate_improvement():
    global Age_list
    global Income_by_90
    global constants
    global cust_constants
    global income_by_90_2
    global improvement
    improvement = {}
    for t in constants.Types_of_AA:
        improvement[t] = [0,0,0,0]
        improvement[t][1] = Income_by_90['Equities']
        improvement[t][3] = Income_by_90[t]
    create_aging(cust_constants.cur_age,cust_constants.Downsize_home_at_age,constants.top_max_age,cust_constants.Expected_retirement_age, cust_constants.Additional_contribution+0.02)
    Allocation_calculations()
    Annual_income_calc()
    calc_resp_ann_income()
    income_by_90_2 = calc_income_by_90()

    for t in constants.Types_of_AA:
        improvement[t][0] = income_by_90_2['Equities']
        improvement[t][2] = income_by_90_2[t]
    return improvement
    
    
##############################################################
#print('started',datetime.now())
class RunningCalculator:
    def __init__(self):
        pass

    def get_the_first_chart(self,path_to_server,cur_age = 35, current_contribution = 4000, Current_super_acct_balance = 45000, \
                 Expected_retirement_age = 65, Additional_contribution = 0, Homeowner =False,married=True,\
                 Value_of_home = 1000000, Downsize_home_at_age = 80 , PVR = 30):
        parse_admin_data(path_to_server)
        parse_customer_data(cur_age, current_contribution , Current_super_acct_balance, \
                 Expected_retirement_age, Additional_contribution, Homeowner ,married,\
                 Value_of_home , Downsize_home_at_age , PVR )
        create_aging(cust_constants.cur_age,cust_constants.Downsize_home_at_age,constants.top_max_age,cust_constants.Expected_retirement_age, cust_constants.Additional_contribution)
        Allocation_calculations()
        Annual_income_calc()
        calc_resp_ann_income()
        inc_by_90 = calc_income_by_90()
        probab_assets = calc_assets()
        return inc_by_90, calculate_cashflow(), probab_assets, new_ret_inc, EI_dict
    def get_the_improvement_chart(self,path_to_server,cur_age = 35, current_contribution = 4000, Current_super_acct_balance = 45000, \
                 Expected_retirement_age = 65, Additional_contribution = 0, Homeowner =False,married=True,\
                 Value_of_home = 1000000, Downsize_home_at_age = 80 , PVR = 30):
        parse_admin_data(path_to_server)
        parse_customer_data(cur_age, current_contribution , Current_super_acct_balance, \
                 Expected_retirement_age, Additional_contribution, Homeowner ,married,\
                 Value_of_home , Downsize_home_at_age , PVR )
        impove_your_income = calculate_improvement()
        return impove_your_income