import json
import pandas as pd 
import random 
import math 
import copy 
import time 


#Parameter has a lower and upper bound - Changes based on mutation
#Also has an allowed range
############################################ PARAMETER CLASS ##################################################
class parameter:
    def __init__(self, name, features_dict):
        self.name = name
        #Give the name of the feature
        feature_dict = features_dict[name]
        #Get type 
        self.type = feature_dict["type"]
        #Get the upper and lower allowable bound for feature value
        self.upper_bound = feature_dict["upper_bound"]
        self.lower_bound = feature_dict["lower_bound"]
        self.range_restriction = feature_dict["range_restriction"]
        self.mutation_amount = feature_dict["mutation_amount"]
        self.present_keys = feature_dict["present_keys"]
        if self.type == "continuous":
            self.mean = feature_dict["mean"]
            self.stdev = feature_dict["stdev"]
        self.random_init()

    def random_init(self):
        if self.type == "continuous" or self.type == "nominal":
            self.random_bounds()
        else:
            self.random_bool()

    def random_bool(self):
        self.upper_bound = random.randint((0,1))
        self.lower_bound = self.upper_bound
    
    def random_bounds(self):
        start_val = self.get_random_value_within_bounds()
        mutation = self.get_bound_change(start_val)
        end_val = start_val + mutation
        if start_val < end_val:
            self.curr_upper_bound = end_val
            self.curr_lower_bound = start_val
        else:
            self.curr_upper_bound = start_val
            self.curr_lower_bound = end_val
        
        
        
    #Return a positive or negative change from a bound start value
    #While does NOT violate the rules. 
    def get_bound_change(self, start_value):
        #Get the mutation amount 
        mutation_amount = self.get_random_mutation_amount()
        if (start_value + mutation_amount) > self.upper_bound:
            #If its the max, change direction
            if start_value == self.upper_bound:
                mutation_amount = mutation_amount*-1
            #Otherwise, set it to the max
            else:
                bound_change = self.upper_bound - start_value
        if (start_value + mutation_amount) < self.lower_bound:
            bound_change = self.lower_bound - start_value

        else:
            bound_change = mutation_amount
        return bound_change
        

    def get_random_mutation_amount(self):
        #Random positive or negative amount
        percent_change = self.mutation_amount[0]/100
        sign = random.choice([-1, 1])
        mutation_val = random.uniform(0, percent_change*self.stdev)
        if self.type == "nominal":
            mutation_val = math.ceil(mutation_val)
        mutation_val = mutation_val * sign 
        return mutation_val

    def get_random_value_within_bounds(self):
        value = random.uniform(self.lower_bound, self.upper_bound)
        if self.type == "nominal":
            value = math.ceil(value)
        return value


    def mutate(self):
        if self.type == "continuous" or self.type == "nominal":
            self.mutate_bounds()
        else:
            self.mutate_bool()

    def mutate_bounds(self):
        old_lower = self.curr_lower_bound
        old_upper = self.curr_upper_bound
        choice = random.choice(["lower", "upper"])
        if choice == "upper":
            change = self.get_bound_change(self.curr_upper_bound)
            self.curr_upper_bound = self.curr_upper_bound + change 
        else:
            change = self.get_bound_change(self.curr_lower_bound)
            self.curr_lower_bound = self.curr_lower_bound + change
        if self.curr_lower_bound > self.curr_upper_bound:
            temp = self.curr_upper_bound
            self.curr_upper_bound = self.curr_lower_bound
            self.curr_lower_bound = temp 

        #If this violates the rules, don't mutate it! 
        if self.upper_bound - self.lower_bound > (self.range_restriction[0]/100)*self.stdev:
            self.curr_lower_bound = old_lower
            self.curr_upper_bound = old_upper

        
    def mutate_bool(self):
        if self.curr_lower_bound == 0:
            self.curr_lower_bound = 1
        else:
            self.curr_lower_bound = 0
        self.curr_upper_bound = self.curr_lower_bound

    def return_bounds(self):
        #Returns lower, upper bound in that order 
        return self.curr_lower_bound, self.curr_upper_bound

    def print_full(self):
        print(f"Name: {self.name}")
        print(f"Type: {self.type}")
        print(f"Min Lower Bound: {self.lower_bound}")
        print(f"Max Upper Bound: {self.upper_bound}")
        print(f"Curr Lower Bound {self.curr_lower_bound}")
        print(f"Curr Upper Bound {self.curr_upper_bound}")
        print(f"Mutation Amount: {self.mutation_amount}")
        print(f"Range Restriction {self.range_restriction}")
        if self.type == "continuous" or self.type == "nominal":
            print(f"Mean {self.mean}")
            print(f"Standard Deviation {self.stdev}")
        print()


    def print_current(self):
        print(f"Curr Lower Bound {self.curr_lower_bound}")
        print(f"Curr Upper Bound {self.curr_upper_bound}")
        print()


        


