import json

import run_experiments 


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
    "sequence_penalty": False,
    "diversify_top_rules": True,
    "reseed_from_best": True,
    "sequence_antecedent_heuristic": True,
    "fitness_function_index": 0,
    "sequence_penalty_index": 0,
    "range_penalty_index": 0
}
npp_named_sites = ['npp_c_cali', 'npp_c_grav', 'npp_c_sand', 'npp_g_basn', 'npp_g_ibpe', 'npp_g_summ', 'npp_m_nort', 'npp_m_rabb', 'npp_m_well', 'npp_p_coll', 'npp_p_smal', 'npp_p_tobo', 'npp_t_east', 'npp_t_tayl', 'npp_t_west']

phase = "Testing"
name = "Test_16"
#npp_named_sites = ['npp_c_cali', 'npp_c_grav']
#npp_named_sites = ['npp_c_cali']
all_data=False

key="frost"
run_experiments.run_experiments(phase, default_parameter_dict, name, npp_named_sites, key=key, all_data=all_data)


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