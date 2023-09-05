import pandas as pd
import pickle 
import numpy as np 

#https://www.dataquest.io/blog/tutorial-add-column-pandas-dataframe-based-on-if-else-condition/
#https://stackoverflow.com/questions/13413590/how-to-drop-rows-of-pandas-dataframe-whose-value-in-a-certain-column-is-nan

separate_data_streams = {
    "temp_hum": ['Air_TempC_Avg', 'Air_TempC_Max', 'Air_TempC_Min', 'Relative_Humidity_Avg', 'Relative_Humidity_Max', 'Relative_Humidity_Min'],
    "rain": ['Ppt_mm_Tot'],
    "wind_speed": ['WS_ms_300cm_Avg', 'WS_ms_300cm_Max', 'WS_ms_150cm_Avg', 'WS_ms_150cm_Max', 'WS_ms_75cm_Avg', 'WS_ms_75cm_Max'],
    "wind_direction": ['WinDir_mean_Resultant', 'WinDir_Std_Dev'],
}

features = ['Air_TempC_Avg', 'Air_TempC_Max', 'Air_TempC_Min', 'Relative_Humidity_Avg', 'Relative_Humidity_Max', 'Relative_Humidity_Min',
'Ppt_mm_Tot', 'WS_ms_300cm_Avg', 'WS_ms_300cm_Max', 'WS_ms_150cm_Avg', 'WS_ms_150cm_Max', 'WS_ms_75cm_Avg', 'WS_ms_75cm_Max',
'WinDir_mean_Resultant', 'WinDir_Std_Dev']

sub_features = ['Air_TempC_Avg', 'Air_TempC_Max', 'Air_TempC_Min', 'Relative_Humidity_Avg', 'Relative_Humidity_Max',
 'Relative_Humidity_Min', 'Ppt_mm_Tot']

key = ["Date_datetime"]
consequent = ["frost"]
npp_named_sites = ['npp_c_cali', 'npp_c_grav', 'npp_c_sand', 'npp_g_basn', 'npp_g_ibpe', 'npp_g_summ', 'npp_m_nort', 'npp_m_rabb', 'npp_m_well', 'npp_p_coll', 'npp_p_smal', 'npp_p_tobo', 'npp_t_east', 'npp_t_tayl', 'npp_t_west']



def create_formatted_csv_from_jornada_df(name, df):
    #Get only the columns we need - features plus Date/Datetime
    keep_cols =  features + key
    modified_features = sub_features + key 
    try:
        df = df[keep_cols]
    except Exception as e:
        print(e)
        df = df[modified_features]
    #Make the next frost column
    df['frost'] = np.where(df["Air_TempC_Min"] <= 0, 1, 0)
    save_name = f"frost_csvs/{name}.csv"
    df.to_csv(save_name)


def make_set():
    for site_name in npp_named_sites:
        pathname = f"pickled_datasets/{site_name}.pkl"
        with open(pathname, "rb") as f:
            site = pickle.load(f)
        create_formatted_csv_from_jornada_df(site_name, site)

#make_set()


def make_shifted_csvs():
    for name in npp_named_sites:
        path = f"frost_csvs/old/{name}.csv"
        df = pd.read_csv(path)
        df["frost"].shift(-1)
        df = df[df["frost"].notna()]
        save_name = f"frost_csvs/{name}.csv"
        df.to_csv(save_name)

#make_shifted_csvs()