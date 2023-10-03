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

#12 runs, 10 rules per run -- store all rules 
#Get the top 10 out of all runs
def best_per_site(file_start, phase, params, runs, max_rules):
    #Here we'll want to separate single rules from ensembles. 
    #For every site:

    save_start = f"{phase}_analysis/"
    if not os.path.exists(save_start):
        os.makedirs(save_start)

    for slice_wise in check_slices:
        if slice_wise == "rule_wise":
            check_index = rules_indexes
        else:
            check_index = ensemble_indexes
        agg_dict = return_aggregate_dict()
        site_rules_dict = {}
        best_rules_list = []
        best_fitness_list = []
        for param in params:
            ##For each run, load in the performance csv
            for run in runs:
                #print("PARAM ", param)
                #print("RUN ", run)
                rules_list = []
                fitness_list = []
                df = pd.read_csv(f"{file_start}{phase}/{phase}_{param}_{run}/rule_predictor_evaluation.csv")
                #Get the best rules models 
                rules_df = df[df["Rule Index"].isin(check_index)]

                for sub_index in check_index:
                    #sub_rule_row = rules_df[df["Rule Index"] == sub_index]
                    sub_rule_row = rules_df.loc[df["Rule Index"] == sub_index]
                    #my_dataframe. loc[my_dataframe["column_name"] == my_value]
                    if not sub_rule_row.empty:
                        rule_dict = make_dict_from_rule_row(sub_rule_row, param, run)
                        rules_list.append(rule_dict)
                        fitness_list.append(rule_dict["metric"])
                if best_rules_list == []:
                    best_rules_list = rules_list
                    best_fitness_list = fitness_list
                else:
                    for i in range(0, len(rules_list)):
                        sub_rule_dict = rules_list[i]
                        if sub_rule_dict["metric"] > min(best_fitness_list):
                            kill_index = best_fitness_list.index(min(best_fitness_list))
                            best_fitness_list.pop(kill_index)
                            best_rules_list.pop(kill_index)
                            best_rules_list.append(sub_rule_dict)
                            best_fitness_list.append(sub_rule_dict["metric"])
                    
            #print(type(best_indexes))
            if slice_wise == "rule_wise":
                for i in range(0, len(best_rules_list)):
                    site_keep_rules = load_rules_or_rule(file_start, phase, best_rules_list[i]["param_index"], best_rules_list[i]["run_index"], best_rules_list[i]["indexes"])
                    site_rules_dict[i] = site_keep_rules
        
        save_agg_name = f'{phase}_analysis/{slice_wise}_aggregate_best_agg.csv'
        save_agg_df = pd.DataFrame(best_rules_list)
        save_agg_df.to_csv(save_agg_name)
        #print(json.dumps(agg_dict, indent=4))
        if slice_wise == "rule_wise":
            rules_save = json.dumps(site_rules_dict, indent=4)
            save_string = f'{phase}_analysis/{slice_wise}_overall_top_rules_agg.json'
            with open(save_string, "w") as f:
                f.write(rules_save)


def save_to_csv(file_name, dict_object):
    df = pd.DataFrame(dict_object)
    df.to_csv(file_name)


def avg_and_best_per_param(file_start, phase, params, runs, max_rules):
    #Here we'll want to separate single rules from ensembles. 
    #For every site:
    avg_dict = {}
    best_dict = {}
    save_start = f"{phase}_analysis/"
    if not os.path.exists(save_start):
        os.makedirs(save_start)

    for slice_wise in check_slices:
        if slice_wise == "rule_wise":
            check_index = rules_indexes
        else:
            check_index = ensemble_indexes
        agg_dict = return_aggregate_dict()
        site_rules_dict = {}
        best_rules_list = []
        best_fitness_list = []
        for param in params:
            ##For each run, load in the performance csv
            param_best_runs = []
            for run in runs:
                #print("PARAM ", param)
                #print("RUN ", run)
                rules_list = []
                fitness_list = []
                df = pd.read_csv(f"{file_start}{phase}/{phase}_{param}_{run}/rule_predictor_evaluation.csv")
                #Get the best rules models 
                rules_df = df[df["Rule Index"].isin(check_index)]
                rules_max = rules_df["F1 Score"].max()
                param_best_runs.append(rules_max)



                # for sub_index in check_index:
                #     #sub_rule_row = rules_df[df["Rule Index"] == sub_index]
                #     sub_rule_row = rules_df.loc[df["Rule Index"] == sub_index]
                #     #my_dataframe. loc[my_dataframe["column_name"] == my_value]
                #     if not sub_rule_row.empty:
                #         rule_dict = make_dict_from_rule_row(sub_rule_row, param, run)
                #         rules_list.append(rule_dict)
                #         fitness_list.append(rule_dict["metric"])
                # if best_rules_list == []:
                #     best_rules_list = rules_list
                #     best_fitness_list = fitness_list
                # else:
                #     for i in range(0, len(rules_list)):
                #         sub_rule_dict = rules_list[i]
                #         if sub_rule_dict["metric"] > min(best_fitness_list):
                #             kill_index = best_fitness_list.index(min(best_fitness_list))
                #             best_fitness_list.pop(kill_index)
                #             best_rules_list.pop(kill_index)
                #             best_rules_list.append(sub_rule_dict)
                #             best_fitness_list.append(sub_rule_dict["metric"])

                    
            avg_dict[param] = [sum(param_best_runs)/len(param_best_runs)]
            best_dict[param] = [max(param_best_runs)]

        avg_name = f'{phase}_analysis/{slice_wise}_average_best_run_param.csv'
        best_name = f'{phase}_analysis/{slice_wise}_best_per_param.csv'
        save_to_csv(avg_name, avg_dict)
        save_to_csv(best_name, best_dict)
        #print(json.dumps(agg_dict, indent=4))


 


rules_indexes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
ensemble_indexes = ["ensemble_avg", "ensemble_or", "ensemble_uniq_avg", "ensemble_uniq_or"]
file_start = "generated_files/"
#phase_name = "Initial_6"
phase_name = "Vital_Initial_E"
param_indexes = [1, 2, 3, 4]
#param_indexes = [1]
#param_indexes = [1]
run_indexes = [1, 2, 3]
#run_indexes = [1]
#sites =['']
max_rules = 10
best_per_site(file_start, phase_name, param_indexes, run_indexes, max_rules)
avg_and_best_per_param(file_start, phase_name, param_indexes, run_indexes, max_rules)



