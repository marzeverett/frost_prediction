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
    "top_rules": 3,
    "generations": 3
}

consequent_dict = {
    "name": "frost",
    "type": "boolean",
    "upper_bound": 1,
    "lower_bound": 1
}

key = "frost" 

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




df = pd.read_csv("frost_csvs/npp_c_cali.csv")
#features_dict = calc_parameters(list_features_dict, default_parameter_dict, df, key)
#print(json.dumps(features_dict, indent=4))






pop = ga_population.population(default_parameter_dict, consequent_dict, list_features_dict, key, df)
pop.run_experiment()

