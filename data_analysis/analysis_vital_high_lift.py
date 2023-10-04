import pandas as pd
import json 
import os



#FOLDER
#{phase_name}/{phase_name}_{param_index}_{run}_{site}
#rule_predictor_evaluation.csv
#top_rules.json
#all_rules.json

#Rule Index, Accuracy, True_Negatives, False_Positives, False_Negatives, True_Positives, Precision, Recall, F1 Score
#Rules indexes 0-14
#Ensemble Indexes: ensemble_avg, ensemble_or, ensemble_uniq_avg, ensemble_uniq_or 

#rules_indexes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def return_best_dict():
    best_dict = {
    "rule_wise": {
        "best_index": [],
        "param_index": [],
        "run": [],
        "f1": [],
        "accuracy": [],
        "false_negatives": [],
        "average_f1": [],
    },
    "ensemble_wise": {
        "best_index": [],
        "param_index": [],
        "run": [],
        "f1": [],
        "accuracy": [],
        "false_negatives": [],
        "average_f1": [],
    }

    }
    return best_dict.copy()


def return_aggregate_dict():
    aggregate_dict = {
        "site": [],
        "metric": [],
        "param_index": [],
        "run_index": [],
        "indexes": [],
        "accuracies": [],
        "false_negatives": [],
        "average_f1": [],
    }
    return aggregate_dict.copy()


def load_rules_or_rule(filestart, phase, param, run, indexes):
    keep_rules_list = []
    filename = f"{file_start}{phase}/{phase}_{param}_{run}/top_rules.json"
    with open(filename) as f:
        rules_list = json.load(f)
    for index in indexes:
        keep_rules_list.append(rules_list[int(index)])
    return keep_rules_list


def get_high_lift_rules_from_list(filestart, phase, param, run, threshold):
    keep_rules_list = []
    filename = f"{file_start}{phase}/{phase}_{param}_{run}/top_rules.json"
    with open(filename) as f:
        rules_list = json.load(f)
    for single_rule in rules_list: 
        if single_rule["lift"] >= threshold and single_rule["support"] >= 0.01:
            keep_rules_list.append(single_rule)
    return keep_rules_list



check_slices = ["rule_wise", "ensemble_wise"]


def make_dict_from_rule_row(rule_row, param_index, run_index):
    rule_dict = {}
    rule_dict["metric"] = rule_row["F1 Score"].item()
    rule_dict["param_index"] = param_index
    rule_dict["run_index"] = run_index
    best_indexes = rule_row["Rule Index"].item()
    rule_dict["indexes"] = best_indexes
    rule_dict["accuracies"] = rule_row["Accuracy"].item()
    rule_dict["false_negatives"] = rule_row["False_Negatives"].item()
    rule_dict["false_positives"] = rule_row["False_Positives"].item()
    rule_dict["true_positives"] = rule_row["True_Positives"].item()
    rule_dict["true_negatives"] = rule_row["True_Negatives"].item() 
    return rule_dict


def save_to_csv(file_name, dict_object):
    df = pd.DataFrame(dict_object)
    df.to_csv(file_name)


#12 runs, 10 rules per run -- store all rules 
#Get the top 10 out of all runs
def get_high_lift_rules(file_start, phase, params, runs, threshold):
    #Here we'll want to separate single rules from ensembles. 
    #For every site:

    save_start = f"{phase}_analysis/"
    if not os.path.exists(save_start):
        os.makedirs(save_start)
    slice_wise = "rules_wise"
    if slice_wise == "rule_wise":
        check_index = rules_indexes
    else:
        check_index = ensemble_indexes

    best_rules_dict = {}
    best_rules = []
    for param in params:
        ##For each run, load in the performance csv
        for run in runs:
            #print("PARAM ", param)
            #print("RUN ", run)
            sub_best_rules = get_high_lift_rules_from_list(file_start, phase, param, run, threshold)
            best_rules = best_rules + sub_best_rules
    rules_save = json.dumps(best_rules, indent=4)
    save_string = f'{phase}_analysis/high_lift_top_rules.json'
    with open(save_string, "w") as f:
        f.write(rules_save)






threshold = 1.6 
rules_indexes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
ensemble_indexes = ["ensemble_avg", "ensemble_or", "ensemble_uniq_avg", "ensemble_uniq_or"]
file_start = "generated_files/"
#phase_name = "Initial_6"
phase_name = "Vital_Initial_F"
param_indexes = [1, 2, 3, 4]
#param_indexes = [1]
#param_indexes = [1]
run_indexes = [1, 2, 3]
#run_indexes = [1]
#sites =['']
max_rules = 10
get_high_lift_rules(file_start, phase_name, param_indexes, run_indexes, threshold)



