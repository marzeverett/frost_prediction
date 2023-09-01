import json
import pandas as pd 
import random 
import math 
import copy 


#######################       RULE CLASS             #########################################
class rule:
    def __init__(self, default_parameter_dict, features_dict, precedent):
        self.features_dict = features_dict.copy()

        self.mutation_rate = default_parameter_dict["mutation_rate"]
        
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

