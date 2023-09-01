import json
import pandas as pd 
import random 
import math 
import copy 



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

