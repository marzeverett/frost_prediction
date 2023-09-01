import json
import pandas as pd 
import random 
import math 
import copy 

#Help from here:
#Normalization: 
#https://www.digitalocean.com/community/tutorials/normalize-data-in-python 
#Coding the cracking variable: https://stackoverflow.com/questions/40901770/is-there-a-simple-way-to-change-a-column-of-yes-no-to-1-0-in-a-pandas-dataframe 
#Random: https://pynative.com/python-random-randrange/
#https://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python 
#QARM
#https://www.ibm.com/docs/fi/db2/9.7?topic=associations-support-in-association-rule 
#Help with sorting a class:
#https://stackoverflow.com/questions/4010322/sort-a-list-of-class-instances-python 



# V1: 
# The data show a definitve screening design to evaluate the the influence of six factors (laser beam power (W), welding speed (m/min), angular position in welding direction (°), focal positon (mm), gas flow rate (l/min), material thickness of the steel sheet (mm)) in three levels and 18 parameter combinations on the weld depth and the geometrical dimensions of the weld metal in laser welded steel-copper joints in the lap configuration with steel on the top side. Every parameter combination was repeated 5 times and every sheet was cuttet 4 times to overall generate 360 cross sections. Every line in the dataset stands for a cross section which was evaluated regarding the dimensions of the weld metal. Additionally, there was a dichotomous data column added for cracking in the weld metal (yes/no). 
# The dataset is not suitable for modelling a precise predicting model of weld depth in the copper sheet, but shows a correlation between cracking (yes/no) and the weld depth in the copper sheet. This can be discribed very well in a binominal logistic regression.
# Moreover the average crack lenght and count of cracks was added in Versions V1.1 

#six factors (laser beam power (W), welding speed (m/min), angular position in welding direction (°), focal positon (mm), gas flow rate (l/min), material thickness of the steel sheet (mm))



csv_path = "/home/marz/Documents/ai_research/manufacturing/Screening datasets for laser welded steel-copper lap joints/V1 and V2/"

load_path = csv_path+"V1_joints.csv"

#Old
parameters = ["power (W)", "welding speed (m/min)", "gas flow rate (l/min)", "focal position (mm)", "angular position (°)", "material thickness (mm)", "cracking in the weld metal"]

parameters = ["power (W)", "welding speed (m/min)", "gas flow rate (l/min)", "focal position (mm)", "angular position (°)", "material thickness (mm)", "cracking in the weld metal", "weld depth copper (µm)"]


mod_parameters = ["power (W)", "welding speed (m/min)", "gas flow rate (l/min)", "focal position (mm)", "angular position (°)", "material thickness (mm)"]




def load_in():
    df = pd.read_csv(load_path)
    df["cracking in the weld metal"] = df["cracking in the weld metal"].map(dict(yes=1, no=0))
    #print(df.head())
    return df 


df = load_in()

yes = df.loc[df["cracking in the weld metal"] == 1]

print(len(yes.index))

print(df.columns)



