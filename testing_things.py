import json

import run_experiments 
import vital_run_experiments


# default_parameter_dict = {
#     "mutation_rate": 20,
#     "mutation_amount": 20,
#     "range_restriction": False,
#     "range_penalty": True,
#     "initial_rule_limit": 2,
#     "index_key": "Date_datetime",
#     "add_subtract_percent": 30,
#     "change_percent": 70,
#     "max_mutation_tries": 5,
#     "population_size": 20, 
#     "top_rules": 4,
#     "generations": 20,
#     "tournament_size": 4,
#     "dominance": True,
#     "sequence": True,
#     "sequence_limit": 12,
#     "sequence_penalty": False,
#     "diversify_top_rules": True,
#     "reseed_from_best": True,
#     "sequence_antecedent_heuristic": False,
#     "fitness_function_index": 0,
#     "sequence_penalty_index": 0,
#     "range_penalty_index": 0
# }

#Was on 0 b4 

default_parameter_dict = {
    "mutation_rate": 20,
    "mutation_amount": 20,
    "range_restriction": False,
    "range_penalty": True,
    "initial_rule_limit": 2,
    "index_key": "Date_datetime",
    "add_subtract_percent": 30,
    "change_percent": 70,
    "max_mutation_tries": 5,
    "population_size": 20, 
    "top_rules": 10,
    "generations": 20,
    "tournament_size": 4,
    "dominance": True,
    "sequence": True,
    "sequence_limit": 12,
    "sequence_penalty": True,
    "diversify_top_rules": True,
    "reseed_from_best": True,
    "sequence_antecedent_heuristic": False,
    "fitness_function_index": 2,
    "sequence_penalty_index": 2,
    "range_penalty_index": 0
}





npp_named_sites = ['npp_c_cali', 'npp_c_grav', 'npp_c_sand', 'npp_g_basn', 'npp_g_ibpe', 'npp_g_summ', 'npp_m_nort', 'npp_m_rabb', 'npp_m_well', 'npp_p_coll', 'npp_p_smal', 'npp_p_tobo', 'npp_t_east', 'npp_t_tayl', 'npp_t_west']
npp_named_sites = ["npp_c_cali"]
phase = "Testing"
name = "Test_22"

#Jornada
#npp_named_sites = ['npp_c_cali', 'npp_c_grav']
#npp_named_sites = ['npp_c_cali']
#all_data=False
# key="frost"
# run_experiments.run_experiments(phase, default_parameter_dict, name, npp_named_sites, key=key, all_data=all_data)


#Vital 
#key = "gluc_risk"
key = "emop"
cases = ["3719", "1292", "2327"]
cases = ["3719", "1292", "2327", "5018", "6009", "1820", "4255", "1191", "1959", "553", "3631", "2738", "818", "1590", "4283", "5693", "3524", "4684", "5837", "1231", "3930", "2267", "4573", "5983", "2272", "6246", "5607", "1900", "3694", "1785", "1018", "251"]

all_data = False
df_list = True
sequence = True
vital_run_experiments.run_experiments(phase, default_parameter_dict, name, cases, key=key, all_data=all_data, df_list=True, sequence=True)


# default_parameter_dict = {
#     "mutation_rate": 20,
#     "mutation_amount": 20,
#     "range_restriction": 300,
#     "index_key": "Date_datetime",
#     "add_subtract_percent": 30,
#     "change_percent": 70,
#     #"add_subtract_percent": 50,
#     #"change_percent": 50,
#     "max_mutation_tries": 10,
#     "population_size": 150, 
#     "top_rules": 5,
#     "generations": 5,
#     "tournament_size": 15,
#     "dominance": True,
#     "sequence": True,
#     "sequence_limit": 10 
# }

# default_parameter_dict = {
#     "mutation_rate": 20,
#     "mutation_amount": 20,
#     "range_restriction": 300,
#     "initial_rule_limit": 2,
#     "index_key": "Date_datetime",
#     "add_subtract_percent": 30,
#     "change_percent": 70,
#     #"add_subtract_percent": 50,
#     #"change_percent": 50,
#     "max_mutation_tries": 10,
#     "population_size": 80, 
#     "top_rules": 10,
#     "generations": 30,
#     "tournament_size": 4,
#     "dominance": True,
#     "sequence": True,
#     "sequence_limit": 10 
# }