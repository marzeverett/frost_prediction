import json
import vital_run_experiments 

param_dict_1 = {
    "mutation_rate": 20,
    "mutation_amount": 20,
    "range_restriction": False,
    "range_penalty": True,
    "initial_rule_limit": 2,
    "index_key": "Date_datetime",
    "add_subtract_percent": 30,
    "change_percent": 70,
    "max_mutation_tries": 5,
    "population_size": 150, 
    "top_rules": 10,
    "generations": 150,
    "tournament_size": 4,
    "dominance": True,
    "sequence": False,
    "sequence_limit": False,
    "sequence_penalty": False,
    "diversify_top_rules": True,
    "reseed_from_best": False,
    "sequence_antecedent_heuristic": False,
    "fitness_function_index": 3,
    "sequence_penalty_index": 2,
    "range_penalty_index": 0
}

param_dict_2 = {
    "mutation_rate": 20,
    "mutation_amount": 20,
    "range_restriction": False,
    "range_penalty": True,
    "initial_rule_limit": 2,
    "index_key": "Date_datetime",
    "add_subtract_percent": 30,
    "change_percent": 70,
    "max_mutation_tries": 5,
    "population_size": 150, 
    "top_rules": 10,
    "generations": 150,
    "tournament_size": 4,
    "dominance": True,
    "sequence": False,
    "sequence_limit": False,
    "sequence_penalty": False,
    "diversify_top_rules": True,
    "reseed_from_best": False,
    "sequence_antecedent_heuristic": False,
    "fitness_function_index": 3,
    "sequence_penalty_index": 3,
    "range_penalty_index": 0
}

param_dict_3 = {
    "mutation_rate": 20,
    "mutation_amount": 20,
    "range_restriction": False,
    "range_penalty": True,
    "initial_rule_limit": 2,
    "index_key": "Date_datetime",
    "add_subtract_percent": 30,
    "change_percent": 70,
    "max_mutation_tries": 5,
    "population_size": 150, 
    "top_rules": 10,
    "generations": 150,
    "tournament_size": 4,
    "dominance": True,
    "sequence": False,
    "sequence_limit": False,
    "sequence_penalty": False,
    "diversify_top_rules": True,
    "reseed_from_best": False,
    "sequence_antecedent_heuristic": False,
    "fitness_function_index": 5,
    "sequence_penalty_index": 2,
    "range_penalty_index": 0
}

param_dict_4 = {
    "mutation_rate": 20,
    "mutation_amount": 20,
    "range_restriction": False,
    "range_penalty": True,
    "initial_rule_limit": 2,
    "index_key": "Date_datetime",
    "add_subtract_percent": 30,
    "change_percent": 70,
    "max_mutation_tries": 5,
    "population_size": 150, 
    "top_rules": 10,
    "generations": 150,
    "tournament_size": 4,
    "dominance": True,
    "sequence": False,
    "sequence_limit": False,
    "sequence_penalty": False,
    "diversify_top_rules": True,
    "reseed_from_best": False,
    "sequence_antecedent_heuristic": False,
    "fitness_function_index": 5,
    "sequence_penalty_index": 3,
    "range_penalty_index": 0
}

cases = ["3719", "1292", "2327", "5018", "6009", "1820", "4255", "1191", "1959", "553", "3631", "2738", "818", "1590", "4283", "5693", "3524", "4684", "5837", "1231", "3930", "2267", "4573", "5983", "2272", "6246", "5607", "1900", "3694", "1785", "1018", "251"]

runs = {
    "1": "1",
    "2": "2",
    "3": "3"
    }
params_dicts = {
    "1": param_dict_1,
    "2": param_dict_2,
    "3": param_dict_3,
    "4": param_dict_4
}

#NAME - {phase_name}_{parameter_index}_{Run}
phase_name = "Vital_Initial_A"
key="gluc_risk"
df_list=True
#cases = ["3719", "1292", "2327", "5018", "6009", "1820", "4255", "1191", "1959", "553", "3631", "2738", "818", "1590", "4283", "5693", "3524", "4684", "5837", "1231", "3930", "2267", "4573", "5983", "2272", "6246", "5607", "1900", "3694", "1785", "1018", "251"]

for param_dict_index in list(params_dicts.keys()):
    for run_index in list(runs.keys()):
            name = f'{phase_name}_{param_dict_index}_{run_index}'
            sequence_val = params_dicts[param_dict_index]["sequence"]
            vital_run_experiments.run_experiments(phase_name, params_dicts[param_dict_index], name, cases, key=key, sequence=sequence_val, df_list=df_list)
