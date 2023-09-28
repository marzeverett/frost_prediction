import pandas as pd 
import math 
import ga_population
import ga_predictor 

#Help from here: https://www.geeksforgeeks.org/python-intersection-two-lists/


filename = f"test/test_A/"
key="frost"
sequence=True

df_path = f"frost_csvs/npp_c_cali.csv"
df = pd.read_csv(df_path)
#print(list_features_dict)
#Split into training and test df 
num_rows = len(df.index)
#0.1 - 10 percent training set - kind of a magic number 
split_index = num_rows - math.ceil(num_rows*0.2)
train_df = df.iloc[:split_index, :]
test_df = df.iloc[split_index:, :]
test_df = test_df.reset_index()

ga_predictor.complete_eval_top_rules(filename, key, test_df, sequence=sequence)




