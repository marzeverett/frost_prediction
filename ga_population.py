import json
import pandas as pd 
import random 
import math 
import copy 
#from copy import deepcopy
import ga_rule
import os 
#d = deepcopy(c



################################################# POPULATION CLASS ###################################################################
#How many top rules to hold? 
#10% hyperparameter of number of rules to hold in top 
#See first if we can init these rules, then worry about scoring them and making new populations 
class population:
    def __init__(self, default_parameter_dict, consequent_dict, feature_dict, key, df):
        #Passes parameters
        self.df = df 
        self.default_parameter_dict = default_parameter_dict.copy()
        self.consequent_dict = consequent_dict.copy()
        self.key = key 
        self.features_dict = self.calc_parameters(feature_dict, self.default_parameter_dict, self.df, self.key)
        self.consequent_support, self.num_consequent = self.calc_consequent_support(self.consequent_dict, self.df)
        self.mutation_rate = self.default_parameter_dict['mutation_rate']
        self.population_size = self.default_parameter_dict["population_size"]
        self.num_top_rules = self.default_parameter_dict["top_rules"]
        self.generations = self.default_parameter_dict["generations"]
        self.mutation_number = math.ceil(self.population_size*(self.mutation_rate/100))
        
        #List of rules 
        self.rules_pop = self.init_rules_pop()
        self.top_rules = []

        #Dominance Dict 
        self.dominance_dict = {}
        self.dominance_fitness_dict = {}
        
    

    def init_rules_pop(self):
        rules_pop = []
        for i in range(0, self.population_size):
            new_rule = ga_rule.rule(self.default_parameter_dict, self.features_dict, self.consequent_dict, self.consequent_support, self.num_consequent, self.df)
            #new_rule.random_init()
            rules_pop.append(new_rule)
        return rules_pop

    def calc_consequent_support(self, consequent_dict, df):
        param_name = consequent_dict['name']
        lower_bound = consequent_dict['lower_bound']
        upper_bound = consequent_dict['upper_bound']
        query = f'{param_name} >= {lower_bound} & {param_name} <= {upper_bound}'
        sub_df = df.eval(query)
        num_consequent = sub_df.sum()
        consequent_support = num_consequent/len(df.index)
        return consequent_support, num_consequent 


    def calc_parameters(self, feature_dict, default_parameter_dict, df, key):
        #For each 
        for item in list(feature_dict.keys()):
            feature = feature_dict[item]
            #Load in defaults that aren't already present 
            if "name" not in list(feature.keys()):
                feature["name"] = item
            if "mutation_amount" not in list(feature.keys()):
                feature["mutation_amount"] = default_parameter_dict["mutation_amount"]
            if "range_restriction" not in list(feature.keys()):
                feature["range_restriction"] = default_parameter_dict["range_restriction"]
            if "max_mutation_tries" not in list(feature.keys()):
                feature["max_mutation_tries"] = default_parameter_dict["max_mutation_tries"]
            #Get max and min value for feature if they were not provided
            if "lower_bound" not in list(feature.keys()):
                feature["lower_bound"] = df[feature["name"]].min()
            if "upper_bound" not in list(feature.keys()):
                feature["upper_bound"] = df[feature["name"]].max()   
            #If continuous, calculate mean and stdev 
            #NOTE: Not actually sure this would work for a nominal variable? 
            if feature["type"] == "continuous" or feature["type"] == "nominal":
                feature["mean"] = df[feature["name"]].mean() 
                feature["stdev"] = df[feature["name"]].std() 
            #Add the keys were the feature is present
            #Need to fix this part 
            df_keys = df[~df[feature["name"]].isna()]
        return feature_dict

    

    def update_top_rules(self):
        #get the top rules in the generation
        self.rules_pop.sort(reverse=True)
        #Get the top keep rules from this population:
        self.pop_top_rules = copy.deepcopy(self.rules_pop[:self.num_top_rules])
        new_pop_top_rules = []
        if self.top_rules == []:
            self.top_rules = copy.deepcopy(self.pop_top_rules)
        #SO UGLY - CHECK 
        else:
            for rule in self.pop_top_rules:
                #Assume not same
                same = False
                for other_rule in self.top_rules:
                    active_params = rule.get_active_parameters()
                    other_active_params = other_rule.get_active_parameters()
                    bounds = rule.get_bounds_list()
                    other_bounds = other_rule.get_bounds_list()
                    if active_params == other_active_params and bounds == other_bounds:
                        same = True
                if not same:
                    new_pop_top_rules.append(rule)
                    
            temp_top_list = self.top_rules + new_pop_top_rules
            temp_top_list.sort(reverse=True)
            self.top_rules = copy.deepcopy(temp_top_list[:self.num_top_rules])
            #print(len(self.top_rules))

    def mutate_population(self):
        mutate_rules = random.sample(self.rules_pop, self.mutation_number)        
        for rule in mutate_rules:
            #print(rule.print_self())
            rule.mutate(self.df)

    def update_dominance_dict(self):
        #Dominance rules need to have lower fitness to be killed, I think 
        for rule in self.rules_pop:
            rule_dict = rule.get_rule_dict()
            #Make its parameters a string - sort alpha so always same
            rule_string = str(sorted(list(rule_dict.keys())))
            #If we don't have an entry for this, make one
            if rule_string not in list(self.dominance_dict.keys()):
                self.dominance_dict[rule_string] = copy.deepcopy(rule_dict)
                self.dominance_fitness_dict[rule_string] = rule.get_fitness()
            #Otherwise:
            else:
                compare_rule_dict = self.dominance_dict[rule_string]
                dominated = True
                for param in list(rule_dict.keys()):
                    #But if it is NOT dominated on anything:
                    if rule_dict[param].upper_bound > compare_rule_dict[param].upper_bound and rule_dict[param].lower_bound < compare_rule_dict[param].lower_bound:
                        dominated = False
                if dominated == False:
                    self.dominance_dict[rule_string] = copy.deepcopy(rule_dict)
                    self.dominance_fitness_dict[rule_string] = rule.get_fitness()


    def kill_dominated(self):
        new_rules_pop_list = []
        for rule in self.rules_pop:
            rule_dict = rule.get_rule_dict()
            #Make its parameters a string - sort alpha so always same
            rule_string = str(sorted(list(rule_dict.keys())))
            #print(rule_string)
            compare_rule_dict = self.dominance_dict[rule_string]
            #Assume dominated
            dominated = True
            for param in list(rule_dict.keys()):
                #But if it is NOT dominated on anything:
                if rule_dict[param].curr_upper_bound >= compare_rule_dict[param].curr_upper_bound and rule_dict[param].curr_lower_bound <= compare_rule_dict[param].curr_lower_bound:
                    dominated = False
            if dominated == False:
                self.dominance_dict[rule_string] = copy.deepcopy(rule_dict)
            #Add it if it's fitness is higher!
            if dominated:
                #Only keep if it has a higher fitness
                if rule.fitness >= self.dominance_fitness_dict[rule_string]:
                    new_rules_pop_list.append(rule)
                else:
                    #print("Killing ")
                    #rule.elegant_print()
                    pass 
            else:
                new_rules_pop_list.append(rule)
        self.rules_pop = new_rules_pop_list


    #NOTE: YOU MIGHT WANT TO DELETE 0 FITNESS INDIVIDUALS
    def run_generation(self):
        #Update dominance dict and Kill dominated rules
        self.update_dominance_dict()
        self.kill_dominated()
        #Update the top rules
        self.update_top_rules()
        #Replace dead population members
        num_replacements = self.population_size - len(self.rules_pop)
        for i in range(0, num_replacements):
            #How will we make the next seed?
            #Magic NUMBER ALERT - CHECK 
            seed = kind_of_mutation = random.choices(["best", "new"], weights=[10, 90], k=1)[0]
            if seed == "best":
                new_rule = copy.deepcopy(random.choice(self.top_rules))
            else:
                new_rule = new_rule = ga_rule.rule(self.default_parameter_dict, self.features_dict, self.consequent_dict, self.consequent_support, self.num_consequent, self.df)
            self.rules_pop.append(new_rule)
        #Create the next generation
        #Note: What's the plan here? 
        #Mutate percentage of population
        self.mutate_population() 


    def save_top_rules(self, name=None):
        list_of_rules = []
        for rule in self.top_rules:
            list_of_rules.append(rule.get_rule_dict_all_numeric())
        rule_save = json.dumps(list_of_rules, indent=4)
        start_string = f"generated_files/{name}/"
        if not os.path.exists(start_string):
            os.makedirs(start_string)
        save_string = f"{start_string}top_rules.json"
        with open(save_string, "w") as f:
            f.write(rule_save) 


    def save_all_rules(self, name=None):
        list_of_rules = []
        for rule in self.rules_pop:
            list_of_rules.append(rule.get_rule_dict_all_numeric())
        rule_save = json.dumps(list_of_rules, indent=4)
        start_string = f"generated_files/{name}/"
        if not os.path.exists(start_string):
            os.makedirs(start_string)
        save_string = f"{start_string}all_rules.json"
        with open(save_string, "w") as f:
            f.write(rule_save) 


    def run_experiment(self, status=False, name=None):
        #Run the generations 
        for i in range(0, self.generations):
            if status:
                print(f" Generation {i}")
            self.run_generation()
        #Save the rules 
        self.save_top_rules(name=name)
        self.save_all_rules(name=name)

    def print_self(self):
        print(f"Pop size: ", self.population_size)
        print(f"Number of top rules to retain: ", self.num_top_rules)
        
    def print_rules(self):
        print("Rules: ")
        for item in self.rules_pop:
            item.print_self()

    def print_rules_and_fitness(self):
        print("Rules: ")
        for item in self.rules_pop:
            item.print_self()
            item.print_fitness_metrics()
            print()

    
    def print_top_rules_and_fitness(self):
        print("Global top rules metrics")
        for rule in self.top_rules:
            rule.elegant_print()
            rule.print_fitness_metrics()
            print()

    def print_dominance_dict(self):
        for item in list(self.dominance_dict.keys()):
            print(self.dominance_dict[item].keys())

    # def print_global_top_rules_metrics(self):
    #     print("Global top rules metrics")
    #     for rule in self.global_top_rules:
    #         rule.print_metrics()

