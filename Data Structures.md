# Data Structures

## Dataframe:
Contains ALL the data for the given task. 
Assumptions:
* Data is all-numeric. Boolean values should be 0 or 1. Categorical variables should be coded.  

## Global Parameter Dict 
Contains:
(Required: The following MUST be provided)
* mutation_rate: Upper and Lower Bound (Can be the same) of amount of individuals in a population to mutate 
* mutation_amount: Upper and Lower Bound (Can be the same) for percent amount of mutation. By default, the upper and lower bound are percentages of the standard deviation for that metric. 
* range_restriction: upper, lower bound (can be same) of % of stdev of range to constrain value in. Only valid for continuous values.


## Feature-Specific Parameter Dict
Contains:  
(Required: The following MUST be provided per-feature)
* name: Name of the feature in question. Should be the same name of the column in the associated data frame. 
* type: continuous, nominal, or boolean. Continuous can take any value within a range. Nominal is a discrete number within a range. Boolean is 1 (True) or 0 (False)
(Optional: You can provide this, or it can be overrided by a global parameter or by dataframe-specific calculation, depending on the type of variable)
* upper_bound: The maximum value the parameter can take (inclusive). If not passed in, it will be calculated from the dataframe. 
* lower_bound" The minimum value the parameter can take (inclusive). If not passed in, it will be calculated from the dataframe. 
* mutation_amount: upper and lower bound for % of stdev the parameter can take. If not passed in, will default to the global parameter dict.
NOTE: You need to figure out a way to make the mutation rate be based on something else, methinks? 
* range restriction: (See global parameter dict)

(Added: These are added by calculation by the system)
* mean: Mean value of feature (if continuous)
* mode: 
* maximum: max value of feature
* minimum: min value of feature
* stdev: standard deviation of feature 
* mutation_method: (Fill in later)
* included_records: List of key values of records in main dataframe that contain the parameter. (Might be "ALL"?)


## Consequent Dict 
Contains:
(Required)
* name of parameter consequent
* type: (same as feature)
* upper_bound: upper bound of interval of interest
* lower_bound: lower bound of interval of interest 
(Added)
included_records: List of key values of records in main dataframe that contains the feature in this range. 


## Mutation Methods
### Continous Variable
Upper and lower value are percent of standard deviation it can mutate from (positive or negative). Random percent is selected from the range (max or min), and applied to the parameter. If the amount is outside the max or min value, it clips to that value. If the value is already max or min, the mutation percent can only be in the opposite direction. 

### Nominal Variable
Assuming nominal variable is coded (discrete). Stdev is percent of change, rounded to a whole number. Same rules for clipping to max and min and direction of change apply here as to the continuous variable. 

### Boolean Variable
Upper and Lower Bound are percent of chance of flipping its value (0 or 1 or 1 to 0)


## Parameter Class: 

### Initalization: 
Takes in:
    (Required)
    Name: The name of the parameter it should be initialized to
    Feature Specific Dict (calculated parameters)
    (Optional)
    Initial Value: (Otherwise randomly chosen within interval)


        