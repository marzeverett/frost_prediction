import json
import pandas as pd 
import random 
import math 
import copy 

from sklearn import metrics 

#Help from here: https://analyticsindiamag.com/evaluation-metrics-in-ml-ai-for-classification-problems-wpython-code/


#This file is for making a predictor based on a rule. 
#df = pd.read_csv("frost_csvs/npp_c_cali.csv")

def load_rules(filename):
    with open(filename) as f:
        rules_list = json.load(f)
    return rules_list
    #print(json.dumps(rules_list, indent=4))


def build_rule_prediction_query(rule):
        parameters_dict = rule["parameters"]
        query_string = ''
        first = 1
        for param in list(parameters_dict.keys()):
            lower = parameters_dict[param]["lower_bound"]
            upper = parameters_dict[param]["upper_bound"]
            if not first:
                query_string = query_string + ' & '
            query_string = query_string + f'{param} >= {lower} & {param} <= {upper}'
            first = 0
        return query_string


#Takes in a rule, a dataframe (to predict on), and returns predictions.
def get_predictions_from_rule(rule, test_df):
    query = build_rule_prediction_query(rule)
    predict_df = test_df.assign(predictions=test_df.eval(query))
    predict_df["predictions"] = predict_df["predictions"].astype(int)
    return predict_df
 
#Evaluate the prediction model 
def evaluate_prediction_model(predict_df, key, model_index=0):
    eval_dict = {}
    eval_dict["Rule Index"] = model_index
    eval_df = predict_df
    #eval_df.loc[predict_df[key] == eval_df["predictions"], "evaluation"] = 1
    #eval_df.loc[predict_df[key] != eval_df["predictions"], "evaluation"] = 0

    pred = eval_df["predictions"].values.tolist()
    true = eval_df[key].values.tolist()

    eval_dict["Accuracy"] = metrics.accuracy_score(true, pred)
    confusion_matrix = metrics.confusion_matrix(true, pred)
    values_array = confusion_matrix.ravel()
    eval_dict["True_Negatives"] = values_array[0]
    eval_dict["False_Positives"] = values_array[1] 
    eval_dict["False_Negatives"] = values_array[2]
    eval_dict["True_Positives"] = values_array[3]

    eval_dict["Precision"] = metrics.precision_score(true, pred, pos_label=1)
    eval_dict["Recall"] = metrics.recall_score(true, pred, pos_label=1)
    eval_dict["F1 Score"] = metrics.f1_score(true, pred, pos_label=1)

    return eval_dict

def ensemble_learn(list_of_rules, test_df):
    #Get the predictions for each rule in the list
    num_models = len(list_of_rules)
    prediction_list = []
    #Get all the prediction dfs for a single rule 
    for single_rule in list_of_rules:
        sub_df = get_predictions_from_rule(single_rule, test_df)
        #Weight them appropriately
        sub_df["predictions"] = sub_df["predictions"]/num_models
        prediction_list.append(sub_df)

    first_predictions =  prediction_list[0]
    for i in range(1, len(prediction_list)):
        first_predictions["predictions"] = first_predictions["predictions"] + prediction_list[i]["predictions"]
    
    first_predictions.loc[first_predictions["predictions"] >= 0.5, "predictions"] = 1
    first_predictions.loc[first_predictions["predictions"] < 0.5, "predictions"] = 0
    return first_predictions 

def ensemble_learn_or(list_of_rules, test_df):
    #Get the predictions for each rule in the list
    num_models = len(list_of_rules)
    prediction_list = []
    #Get all the prediction dfs for a single rule 
    for single_rule in list_of_rules:
        sub_df = get_predictions_from_rule(single_rule, test_df)
        prediction_list.append(sub_df)

    first_predictions = prediction_list[0]
    for i in range(1, len(prediction_list)):
        first_predictions["predictions"] = first_predictions["predictions"] | prediction_list[i]["predictions"]

    return first_predictions 


def get_unique_fitness_rules(list_of_rules):
    fitness_list = [round(list_of_rules[0]["fitness"], 4)]
    unique_fitness_rules =  [list_of_rules[0]]
    for i in range(1, len(list_of_rules)):
        if round(list_of_rules[i]["fitness"], 4) not in fitness_list:
            fitness_list.append(round(list_of_rules[i]["fitness"], 4))
            unique_fitness_rules.append(list_of_rules[i])
    return unique_fitness_rules


def complete_eval_top_rules(filepath_start, key, df):
    filename = f"{filepath_start}top_rules.json"
    if not os.path.exist(filename):
        os.mkdirs(filename)
    rules_list = load_rules(filename)
    eval_dict_list = []
    #The individual rules 
    model_index = 0
    for rule in rules_list: 
        predict_df = get_predictions_from_rule(rule, df)
        eval_dict = evaluate_prediction_model(predict_df, key, model_index=model_index)
        eval_dict_list.append(eval_dict)
        model_index += 1
    #Ensemble of best rules - average 
    predict_df = ensemble_learn(rules_list, df)
    eval_dict = evaluate_prediction_model(predict_df, key, model_index="ensemble_avg")
    eval_dict_list.append(eval_dict)
    #Ensemble of best rules - Or 
    predict_df = ensemble_learn_or(rules_list, df)
    eval_dict = evaluate_prediction_model(predict_df, key, model_index="ensemble_or")
    eval_dict_list.append(eval_dict)
    #Get best rules with unique fitness 
    best_unique_rules = get_unique_fitness_rules(rules_list)
    #Ensemble of best unique rules - average
    predict_df = ensemble_learn(best_unique_rules, df)
    eval_dict = evaluate_prediction_model(predict_df, key, model_index="ensemble_uniq_avg")
    eval_dict_list.append(eval_dict)
    #Ensemble of best unique rules - or
    predict_df = ensemble_learn_or(best_unique_rules, df)
    eval_dict = evaluate_prediction_model(predict_df, key, model_index="ensemble_uniq_or")
    eval_dict_list.append(eval_dict)

    eval_df = pd.DataFrame(eval_dict_list)
    save_name = f"{filepath_start}rule_predictor_evaluation.csv"
    eval_df.to_csv(save_name)



#print(eval_dict)
#complete_eval_top_rules("generated_files/None/", "frost")