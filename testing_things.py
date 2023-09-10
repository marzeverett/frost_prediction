import json

import run_experiments 


default_parameter_dict = {
    "mutation_rate": 20,
    "mutation_amount": 20,
    "range_restriction": 50,
    "index_key": "Date_datetime",
    "add_subtract_percent": 30,
    "change_percent": 70,
    #"add_subtract_percent": 50,
    #"change_percent": 50,
    "max_mutation_tries": 10,
    "population_size": 20, 
    "top_rules": 15,
    "generations": 2,
    "tournament_size": 15,
    "dominance": True,
    "sequence": True,
    "sequence_limit": 10 
}
#npp_named_sites = ['npp_c_cali', 'npp_c_grav', 'npp_c_sand', 'npp_g_basn', 'npp_g_ibpe', 'npp_g_summ', 'npp_m_nort', 'npp_m_rabb', 'npp_m_well', 'npp_p_coll', 'npp_p_smal', 'npp_p_tobo', 'npp_t_east', 'npp_t_tayl', 'npp_t_west']

phase = "Testing"
name = "Test_4"
#npp_named_sites = ['npp_c_cali', 'npp_c_grav']
npp_named_sites = ['npp_c_cali', 'npp_c_grav']

key="frost"
run_experiments.run_experiments(phase, default_parameter_dict, name, npp_named_sites, key=key, all_data=True)



