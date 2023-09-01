import json
import pandas as pd 
import random 
import math 
import copy 

#Help from here:
#Normalization: 
#https://www.digitalocean.com/community/tutorials/normalize-data-in-python 
#Coding the cracking variable: https://stackoverflow.com/questions/40901770/is-there-a-simple-way-to-change-a-column-of-yes-no-to-1-0-in-a-pandas-dataframe 
#Random: https://pynative.com/python-random-randrange/
#https://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python 
#QARM
#https://www.ibm.com/docs/fi/db2/9.7?topic=associations-support-in-association-rule 
#Help with sorting a class:
#https://stackoverflow.com/questions/4010322/sort-a-list-of-class-instances-python 



# V1: 
# The data show a definitve screening design to evaluate the the influence of six factors (laser beam power (W), welding speed (m/min), angular position in welding direction (°), focal positon (mm), gas flow rate (l/min), material thickness of the steel sheet (mm)) in three levels and 18 parameter combinations on the weld depth and the geometrical dimensions of the weld metal in laser welded steel-copper joints in the lap configuration with steel on the top side. Every parameter combination was repeated 5 times and every sheet was cuttet 4 times to overall generate 360 cross sections. Every line in the dataset stands for a cross section which was evaluated regarding the dimensions of the weld metal. Additionally, there was a dichotomous data column added for cracking in the weld metal (yes/no). 
# The dataset is not suitable for modelling a precise predicting model of weld depth in the copper sheet, but shows a correlation between cracking (yes/no) and the weld depth in the copper sheet. This can be discribed very well in a binominal logistic regression.
# Moreover the average crack lenght and count of cracks was added in Versions V1.1 

#six factors (laser beam power (W), welding speed (m/min), angular position in welding direction (°), focal positon (mm), gas flow rate (l/min), material thickness of the steel sheet (mm))



#csv_path = "/home/maryeverett/Documents/manufacturing/Screening datasets for laser welded steel-copper lap joints/V1 and V2/"
csv_path = "V1 and V2/"


load_path = csv_path+"V1_joints.csv"

parameters = ["power (W)", "welding speed (m/min)", "gas flow rate (l/min)", "focal position (mm)", "angular position (°)", "material thickness (mm)", "cracking in the weld metal"]

mod_parameters = ["power (W)", "welding speed (m/min)", "gas flow rate (l/min)", "focal position (mm)", "angular position (°)", "material thickness (mm)", "weld depth copper (µm)"]


############################################ PARAMETER CLASS ##################################################
class parameter:
    def __init__(self, name, df_row, curr_present=False, curr_upper_bound=None, curr_lower_bound=None, static_val_present=False, static_val=None):
        self.name = name
        #If numerical - may need to fix later
        self.min=df_row.min()
        self.max=df_row.max()
        self.mean=df_row.mean()
        self.median=df_row.median()
        self.mode = df_row.mode()
        self.std = df_row.std()
        #Passed in or not 
        self.curr_present=curr_present
        self.curr_upper_bound=curr_upper_bound
        self.curr_lower_bound=curr_lower_bound
        self.static_val_present=static_val_present
        self.static_val=static_val

    def random_init(self):
        self.curr_present = bool(random.getrandbits(1))
        self.random_init_bounds()

    #This will leave us off somewhere if 
    def random_init_bounds(self):
        within_range = False
        while within_range == False:
            self.set_bounds()
            within_range = self.check_range()

    def set_bounds(self):
        #Check -- 
        item_one = random.uniform(self.min, (self.max-self.min/2))
        item_two = random.uniform(item_one, self.max)
        #print("Item one", item_one)
        #print("Item two", item_two)
        self.curr_lower_bound = item_one
        self.curr_upper_bound = item_two

    def check_range(self): 
        #.2 is our magic number, admittedly 
        if (self.curr_upper_bound-self.curr_lower_bound) > (.5*self.std):
            return False
        else:
            return True

    def mutate_range(self, kind): 
        safe = False
        while safe == False:
            self.change_bound(kind)
            #Check range not too large
            range_check = self.check_range()
            flop_check = self.check_flop()
            if range_check and flop_check:
                safe = True

    def change_bound(self, kind):
        #Change between 5 and 20% of the standard deviation 
        change_amount = random.uniform(0, 0.2*self.std)
        #This might be slow, may want to revisit 
        #This makes the change randomly positive or negative with a 50% chance 
        change_amount = change_amount*random.choice([-1, 1])
        #print("----------------------------------------")
        #print("Name: ", self.name)
        #print("Bound kind", kind)
        #print("Change amount", change_amount)
        #print("Old lower bound ", self.curr_lower_bound)
        #print("Old upper bound ", self.curr_upper_bound)
        if kind == "lower":
            self.curr_lower_bound = self.curr_lower_bound+change_amount
        else:
            self.curr_upper_bound = self.curr_upper_bound+change_amount

        #print("New lower bound ", self.curr_lower_bound)
        #print("New upper bound ", self.curr_upper_bound)

    def check_flop(self):
        if self.curr_lower_bound > self.curr_upper_bound:
            return False
        else:
            return True

    def mutate(self, presence=False, num_in_present=2):
        mutation_options = ["present", "lower", "upper"]
        choice = random.choice(mutation_options)
        #print("Mutation Choice ", choice, "Presence ", presence)
        #print("Name ", self.name)
        #If we are mutating presence or absence, we will flip-flop here 
        if choice == "present" or presence==True:
            #print("before self.curr_present", self.curr_present)
            if self.curr_present:
                if num_in_present > 1:
                    new_presence = False
                else:
                    new_presence = True
            else:
                new_presence = True
            self.curr_present = new_presence
            #print("after self.curr_present", self.curr_present)
        else:
            self.mutate_range(choice)


    def print_self(self):
        print(f"Name: {self.name}")
        #If numerical - may need to fix later
        print(f"Min: {self.min}")
        print(f"Max: {self.max}")
        print(f"Mean: {self.mean}")
        print(f"Median: {self.median}")
        #print(f"Mode: {self.mode}")
        print(f"Std Dev: {self.std}")
        #Passed in or not 
        print(f"Currently present?: {self.curr_present}")
        print(f"Current Upper Bound: {self.curr_upper_bound}")
        print(f"Current Lower Bound: {self.curr_lower_bound}")
        print(f"Static Value Present?: {self.static_val_present}")
        print(f"Static Value: {self.static_val}")

    def print_basics(self): 
        print(f"Name: {self.name}")
        print(f"Currently present?: {self.curr_present}")
        print(f"Current Upper Bound: {self.curr_upper_bound}")
        print(f"Current Lower Bound: {self.curr_lower_bound}")
        print()

    def print_precedent_basics(self):
        print(f"Name: {self.name}")
        print(f"Static Value Present?: {self.static_val_present}")
        print(f"Static Value: {self.static_val}")
        print()
        



#######################       RULE CLASS             #########################################
class rule:
    def __init__(self, df, mod_parameter_pool, precedent=None):
        self.df = df 
        self.mod_parameter_pool = mod_parameter_pool.copy()
        #This will be a list of parameter classes 
        self.antecedent = self.random_init()
        #This will be the precedent of interest 
        self.precedent = precedent
        self.present_antecedent = self.present_params()

        #These are rule metrics 
        self.support = None
        self.support_num = None
        self.confidence = None
        self.lift = None
        self.score = None
        self.num_antecedent=None
        self.num_precedent=None

    def random_init(self):
        antecedent_list = []
        for item in self.mod_parameter_pool:
            param = parameter(item, df[item])
            param.random_init()
            antecedent_list.append(param)
        return antecedent_list

        #Make it random if it is present or not
        #If it is present, make sure 

    def mutate(self): 
        #Pick ONE of the rules in the antecedent
        #Another hyperparameter, but lets make a 70% chance it will mutate a bound
        #And a 30% chance it will change the presence/absence of a rule
        #But lets still limit to one rule? 
        #Might need to fix this, a bit odd 
        self.present_antecedent = self.present_params_mutate()
        #print("Present Before")
        #print(len(self.present_antecedent))
        present_mutation_rule = random.choice(self.present_antecedent)
        all_mutation_rule = random.choice(self.antecedent)
        kind_of_mutation = random.choices(["present", "all"], weights=[70, 30], k=1)[0]
        #Mutate that rule 
        #print("********************Kind of mutation ", kind_of_mutation)
        num_in_present = len(self.present_antecedent)
        #print(num_in_present)
        if kind_of_mutation == "present":
            present_mutation_rule.mutate(presence=False, num_in_present=num_in_present)
        else:
            all_mutation_rule.mutate(presence=True, num_in_present=num_in_present)
        self.present_antecedent = self.present_params_mutate()

    def calc_score(self): 
        #This is where we will fill in confidence, lift, and support! 
        #Figure out exactly how we want to score? 
        #Start with quantminer -- ? or if can't find, start with equal weighting. 
        #Pretty naiive right now! - just adding each 
        #OLD - plain vanilla no special score run 
        #score = self.calc_support_percent() + self.calc_confidence() + self.calc_lift()
        score = 5*self.calc_support_percent() + self.calc_confidence() + 5*(abs(1-self.calc_lift()))

        self.score = score
        return score 

    #Returns list of parameter objects that are actually present 
    def present_params(self):
        return_list = []
        for item in self.antecedent:
            if item.curr_present == True:
                return_list.append(item)
        if len(return_list) > 1:
            actual_list = random.sample(return_list, 2)
            for item in return_list:
                if item not in actual_list:
                    item.curr_present = False
            return actual_list
        #If return list is still empty 
        if return_list == []:
            item = random.choice(self.antecedent)
            item.curr_present = True
            return_list.append(item)
            return return_list
        else:
            return return_list

    def present_params_mutate(self):
        return_list = []
        for item in self.antecedent:
            if item.curr_present == True:
                return_list.append(item)
        return return_list


    def num_containing_antecedent_only(self):
        next_filter = self.df
        for item in self.present_antecedent:
            next_filter = next_filter.loc[(next_filter[item.name] >= item.curr_lower_bound) & (next_filter[item.name] <= item.curr_upper_bound)]
        self.num_antecedent = len(next_filter.index)
        return len(next_filter.index)


    def num_containing_precedent_only(self):
        next_filter = self.df
        if isinstance(self.precedent, list):
            for item in self.precedent:
                next_filter = next_filter.loc[(next_filter[item.name] == item.static_val)]
        else:
            item = self.precedent
            next_filter = next_filter.loc[(next_filter[item.name] == item.static_val)]
        self.num_precedent = len(next_filter.index)
        return len(next_filter.index)

    def calc_support_percent(self):
        #Make it percent of total. 
        #calculate the NUMBER of rules in the database that have the antecedent and precedent which meet the criteria!!! 
        # a / b : 
        # a - number containing ALL items appearing in rule
        # b - total groups considered 
        num_obs = len(self.df)
        next_filter = self.df
        for item in self.present_antecedent:
            next_filter = next_filter.loc[(next_filter[item.name] >= item.curr_lower_bound) & (next_filter[item.name] <= item.curr_upper_bound)]
        if isinstance(self.precedent, list):
            for item in self.precedent:
                next_filter = next_filter.loc[(next_filter[item.name] == item.static_val)]
        else:
            item = self.precedent
            next_filter = next_filter.loc[(next_filter[item.name] == item.static_val)]
        self.support_num = len(next_filter.index)
        self.support = len(next_filter.index)/num_obs
        return len(next_filter.index)/num_obs

    def calc_support_num(self):
        num_obs = len(self.df)
        next_filter = self.df
        for item in self.present_antecedent:
            next_filter = next_filter.loc[(next_filter[item.name] >= item.curr_lower_bound) & (next_filter[item.name] <= item.curr_upper_bound)]
        if isinstance(self.precedent, list):
            for item in self.precedent:
                next_filter = next_filter.loc[(next_filter[item.name] == item.static_val)]
        else:
            item = self.precedent
            next_filter = next_filter.loc[(next_filter[item.name] == item.static_val)]
        self.support_num = len(next_filter.index)
        return len(next_filter.index)

    def calc_confidence(self):
        confidence = 0.0
        #Ratio m/n
        #m - number of groups containing both rule head and rule body
        #n - number of groups containing just rule body 
        m = self.calc_support_num()
        n = self.num_containing_antecedent_only()
        if n > 0:
            confidence =  m/n
        else:
            confidence = 0.0 
        self.confidence = confidence
        return confidence 

    def calc_lift(self):
        lift = 0.0
        conf = self.calc_confidence()
        supp_head = self.num_containing_antecedent_only()
        if supp_head > 0:
            lift =  conf/supp_head
        self.lift = lift
        return lift

    def print_self(self):
        print("RULE: ")
        print("Antecedent")
        for item in self.present_antecedent:
            #item.print_self()
            item.print_basics()
        print("Precedent")
        #self.precedent.print_self()
        self.precedent.print_precedent_basics()

    def print_metrics(self):
        print(f"Support: {self.support}")
        print(f"Confidence: {self.confidence}")
        print(f"Lift: {self.lift}")
        print(f"Overall Score: {self.score}")

    def __lt__(self, other):
        return self.score < other.score



################################################# POPULATION CLASS ###################################################################
#How many top rules to hold? 
#10% hyperparameter of number of rules to hold in top 
#See first if we can init these rules, then worry about scoring them and making new populations 
class population:
    def __init__(self, df, mod_parameters, pop_size, precedent, top_keep=2, mutation_rate=0.2):
        #Passes parameters
        self.df = df 
        self.mod_parameter_pool = self.init_mod_parameter_pool(mod_parameters)
        self.mod_parameter_pool_list = mod_parameters
        self.pop_size = pop_size
        self.top_keep = top_keep
        self.mutation_rate = mutation_rate 
        #Calculated
        self.retain_rules = math.ceil(pop_size*.1)
        self.mutation_number = math.ceil(self.pop_size*self.mutation_rate)
        #List of rules 
        self.rules_pop = self.init_rules_pop()
        self.score_population()
        self.prev_rules_pop = []
        self.global_top_rules = []
        self.global_top_rules_scores = []
        self.top_rules = []
        self.top_rules_scores = []
        self.precedent = precedent
    


    def init_rules_pop(self):
        rules_pop = []
        for i in range(0, self.pop_size):
            new_rule = rule(self.df, self.mod_parameter_pool_list.copy(), precedent=precedent)
            new_rule.random_init()
            rules_pop.append(new_rule)
        return rules_pop

    def score_population(self):
        for rule in self.rules_pop:
            #print("Rule score")
            rule.calc_support_percent()
            rule.calc_confidence()
            rule.calc_lift()
            rule.calc_score()
            #self.print_rules()
            #rule.print_metrics()

    def init_mod_parameter_pool(self, mod_parameters):
        param_pool = []
        for param in mod_parameters:
            param_pool.append(parameter(param, self.df[param]))
        return param_pool
    
    def run_generation(self):
        #Score pop.
        #self.score_population()
        #Top x rules get copied to the top rules list. -- these are automatically kept. 
        self.rules_pop.sort(reverse=True)
        self.top_rules = copy.deepcopy(self.rules_pop[:self.top_keep])
        self.top_rules_scores = [x.score for x in self.top_rules]
        # print("Local-----------------------------")
        # self.print_top_rules_metrics()
        # print("Global-----------------------------")
        # self.print_global_top_rules_metrics()
        #Replace any better rules with global top rules list ]
        temp_list = copy.deepcopy(self.global_top_rules)
        #temp_list = copy.deepcopy(self.global_top_rules) + copy.deepcopy(self.top_rules)

        for rule in self.top_rules:
            if rule.score not in self.global_top_rules_scores:
                temp_list.append(rule)
        temp_list = [*set(temp_list)]
        temp_list.sort(reverse=True)
        self.global_top_rules = copy.deepcopy(temp_list[:self.top_keep])
        self.global_top_rules_scores = [x.score for x in self.global_top_rules]
        #copy current generation to the prev generation - eventually add tournament selection 
        self.prev_rules_pop = copy.deepcopy(self.rules_pop)
        #Mutate any current gen with a score of 0
        for i in range(0, len(self.rules_pop)):
            if self.rules_pop[i].score <= 0.00:
                self.rules_pop[i].mutate()
        #Mutate an additional mutation_rate% (want in-place, so don't copy here)
        mutate_list = random.sample(self.rules_pop, self.mutation_number)
        for rule in mutate_list:
            #print("Before")
            #rule.print_self()
            rule.mutate()
            #print("After")
            #rule.print_self()
        #May add this later!! 
        self.score_population()
        #self.rules_pop[-self.top_keep:] = copy.deepcopy(self.top_rules)

    def save_rules_to_csv(self, name, which="global", k=10):
        if which=="global":
            working_list = self.global_top_rules
        else:
            working_list = self.rules_pop
        #Take top k rules 
        saving_list = working_list[:k]
        all_rules_list = [] 
        for rule in saving_list:
            rule_list = []
            rule_list.append("SCORES: s, c, l, score")
            rule_list.append(rule.support)
            rule_list.append(rule.confidence)
            rule_list.append(rule.lift)
            rule_list.append(rule.score)
            rule_list.append("RULES")
            for item in rule.present_antecedent:
                rule_list.append(item.name)
                rule_list.append(item.curr_lower_bound)
                rule_list.append(item.curr_upper_bound)
            all_rules_list.append(rule_list)

        df = pd.DataFrame(all_rules_list)
        #print(df.head())
        save_name = name+".csv"
        df.to_csv(save_name)


    def run_experiment(self, generations, status=False):
        for i in range(0, generations):
            if status:
                print(f" Generation {i}")
            self.run_generation()
            if status:
                print(f"Global Top rules scores: {self.global_top_rules_scores}")
                print(f"Local Top rules scores: {self.top_rules_scores}")

        #Add back in later!!! 
        print("Global top rules scores")
        print(self.global_top_rules_scores)
        print("Current top rules scores")
        print(self.global_top_rules_scores)
        print("Top Rules: ")
        for rule in self.global_top_rules:
            print()
            rule.print_self()
            rule.print_metrics()
        

    def print_self(self):
        print("Modulation parameters: ")
        for param in self.mod_parameter_pool_list:
            print()
            param.print_self()
        print(f"Pop size: ", self.pop_size)
        print(f"Number of top rules to retain: ", self.retain_rules)
        
    def print_rules(self):
        print("Rules: ")
        for item in self.rules_pop:
            item.print_self()

    def print_top_rules_metrics(self):
        print("Local top rules metrics")
        for rule in self.top_rules:
            rule.print_metrics()

    def print_global_top_rules_metrics(self):
        print("Global top rules metrics")
        for rule in self.global_top_rules:
            rule.print_metrics()


#If you run into issues, make sure you are figuring out 
#if copy is working correctly!!! 

def load_in():
    df = pd.read_csv(load_path)
    df["cracking in the weld metal"] = df["cracking in the weld metal"].map(dict(yes=1, no=0))
    #print(df.head())
    return df 


df = load_in()
precedent = parameter("cracking in the weld metal", df["cracking in the weld metal"], static_val_present=True, static_val=1)

# pop_size = 100
# mutation_rate = 0.2
# top_keep = 10
# generations = 25

pop_size = 200
mutation_rate = 0.2
top_keep = 10
generations = 500


pop = population(df, mod_parameters, pop_size, precedent, mutation_rate=mutation_rate, top_keep=top_keep)

pop.run_experiment(generations, status=False)
pop.save_rules_to_csv("time_5_life_5_time_support_500_gen_200_pop")


