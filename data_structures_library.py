import json
import pandas as pd 
import random 
import math 
import copy 
import time 

#CHANGE 
#import ga_parameter
#import ga_rule
import ga_population

#https://www.statology.org/pandas-select-rows-without-nan/

default_parameter_dict = {
    "mutation_rate": 20,
    "mutation_amount": 20,
    "range_restriction": 50,
    "index_key": "Date_datetime",
    "add_subtract_percent": 30,
    "change_percent": 70,
    "max_mutation_tries": 10,
    "population_size": 20, 
    "top_rules": 3

}
consequent_dict = {
    "name": "frost",
    "type": "boolean",
    "upper_bound": 1,
    "lower_bound": 1
}

key = "Date_datetime" 

list_features_dict = {
    "Air_TempC_Avg": {
        "name": "Air_TempC_Avg",
        "type": "continuous"
    },
    "Air_TempC_Max": {
        "name": "Air_TempC_Max",
        "type": "continuous"
    },
    "Air_TempC_Min": {
        "name": "Air_TempC_Min",
        "type": "continuous"
    },
    "Relative_Humidity_Avg": {
        "name": "Relative_Humidity_Avg",
        "type": "continuous"
    },
    "Relative_Humidity_Max": {
        "name": "Relative_Humidity_Max",
        "type": "continuous"
    },
    "Relative_Humidity_Min": {
        "name": "Relative_Humidity_Min",
        "type": "continuous"
    },
    "Ppt_mm_Tot": {
        "name": "Ppt_mm_Tot",
        "type": "continuous"
    },
    "WS_ms_300cm_Avg": {
        "name": "WS_ms_300cm_Avg",
        "type": "continuous"
    },
    "WS_ms_300cm_Max": {
        "name": "WS_ms_300cm_Max",
        "type": "continuous"
    },
    "WS_ms_150cm_Avg": {
        "name": "WS_ms_150cm_Avg",
        "type": "continuous"
    },
    "WS_ms_150cm_Max": {
        "name": "WS_ms_150cm_Max",
        "type": "continuous"
    },
    "WS_ms_75cm_Avg": {
        "name": "WS_ms_75cm_Avg",
        "type": "continuous"
    },
    "WS_ms_75cm_Max": {
        "name": "WS_ms_75cm_Max",
        "type": "continuous"
    },
    "WinDir_mean_Resultant": {
        "name": "WinDir_mean_Resultant",
        "type": "continuous"
    },
    "WinDir_Std_Dev": {
        "name": "WinDir_Std_Dev",
        "type": "continuous"
    }
}


def calc_parameters(feature_dict, default_parameter_dict, df, key):
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
        #Chance you might want to keep this as a Series and not a list 
        feature["present_keys"] = df_keys[key].values.tolist()
    return feature_dict

df = pd.read_csv("frost_csvs/npp_c_cali.csv")
features_dict = calc_parameters(list_features_dict, default_parameter_dict, df, key)
#print(json.dumps(features_dict, indent=4))



def calc_consequent_support(consequent_dict, df):
    param_name = consequent_dict['name']
    lower_bound = consequent_dict['lower_bound']
    upper_bound = consequent_dict['upper_bound']
    query = f'{param_name} >= {lower_bound} & {param_name} <= {upper_bound}'
    sub_df = df.eval(query)
    num_consequent = sub_df.sum()
    consequent_support = num_consequent/len(df.index)
    return consequent_support, num_consequent 
# #param_name = "WS_ms_75cm_Max"
# param_name = "Air_TempC_Max"
# param = ga_parameter.parameter(param_name, features_dict)
# #param.print_full()
# param.print_current()
# param.mutate()
# param.print_current()


# consequent_support, num_consequent = calc_consequent_support(consequent_dict, df)
# print(consequent_support)
# #Init'ing a rule automatucally calculates its fitness, and so 
# #Does mutating a rule. 
# the_rule = ga_rule.rule(default_parameter_dict, features_dict, consequent_dict, consequent_support, num_consequent, df)
# the_rule.print_self()
# the_rule.mutate(df)
# the_rule.print_self()


pop = ga_population.population(default_parameter_dict, consequent_dict, list_features_dict, key, df)
#pop.print_self()
#pop.print_rules()
#pop.print_rules_and_fitness()
pop.run_generation()
#pop.print_dominance_dict()
pop.print_top_rules_and_fitness()
#time.sleep(5)
print("-------------------------------")
pop.run_generation()
pop.run_generation()
# pop.run_generation()
# pop.run_generation()
# pop.run_generation()
# pop.run_generation()
# pop.run_generation()
# pop.run_generation()
# pop.run_generation()
# pop.run_generation()
# pop.run_generation()
# pop.run_generation()
# pop.run_generation()
pop.print_top_rules_and_fitness()