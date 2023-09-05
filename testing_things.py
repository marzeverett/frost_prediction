import json

import run_experiments 


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
#npp_named_sites = ['npp_c_cali', 'npp_c_grav', 'npp_c_sand', 'npp_g_basn', 'npp_g_ibpe', 'npp_g_summ', 'npp_m_nort', 'npp_m_rabb', 'npp_m_well', 'npp_p_coll', 'npp_p_smal', 'npp_p_tobo', 'npp_t_east', 'npp_t_tayl', 'npp_t_west']


name = "Test_1"
npp_named_sites = ['npp_c_cali', 'npp_c_grav']
key="frost"
run_experiments.run_experiments(default_parameter_dict, name, npp_named_sites, key=key)



