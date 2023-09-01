import json
import pandas as pd 
import random 
import math 
import copy 







#Parameter has a lower and upper bound - Changes based on mutation
#Also has an allowed range
#

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
        


