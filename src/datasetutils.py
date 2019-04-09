import numpy as np
import os
import pandas as pd
import sys

# map a valid datatype for every possible column of the
# dataset
keyword_type_map = {
    'unixtimestamp': np.float64,
    'hhmmss': object,
    'R_BauBGb-P_SUM': np.float64,
    'E_GLOBAL': np.float64,
    'T_AMB': np.float64,
    'P_AIR': np.float64,
    'YYYYMMDD': str,
    'AEZ-P_SUM': np.float64,
    'R_BauTGb-P_SUM': np.float64,
    'PV_SolarLog_30kW-P_SUM': np.float64,
    'PV_120kW-P_SUM': np.float64,
    'R_BauBGa-P_SUM': np.float64,
    'R_Bau_TGa-P_SUM': np.float64	
}

value_limits = {
    # TODO: real limits
    'AEZ-P_SUM': [5, 75],
    'R_BauBGa-P_SUM': [5, 60],
    'R_BauBGb-P_SUM': [5, 40],
    'R_Bau_TGa-P_SUM': [25, 250],
    'R_BauTGb-P_SUM': [25, 275]
}

def apply_type_conversion(df, col_of_interest):
    """
    @param df: the dataframe you want the type conversation
           to be applied
    @return: the same dataframe as input, but with 
             the converted dtypes
    """      
    for col in col_of_interest:
        df[col] = df[col].astype(keyword_type_map[col])


def add_time_columns(df):
    """
    @param df: the dataframe you want to add the columns
    @return: the same dataframe as input, but with new columns
    """    
    df['Month'] = df['YYYYMMDD'].str[4:6].astype(np.float64)
    df['Day'] = df['YYYYMMDD'].str[6:8].astype(np.float64)
    df['Hour'] = df['hhmmss'].str[0:2].astype(np.float64)


def contains_error(val):    
    """
    @param val: the value you want to check for errors
    @return: if no error: input, if error: NaN
    """
    if 'err' in "{}".format(val):
        return np.nan
    else:
        return val

def apply_limits(df, col_of_interest):    
    """
    @param df: the dataframe you want the limits to be applied
    @param col_of_interest: the columns you want the limits to
           be applied.
    @return: the same dataframe as input, but with NaN in case
             of limit violations
    """    
    for col in col_of_interest:
        if not col in value_limits:
            # we only can apply limits if there are any defined
            continue

        df[df[col] < value_limits[col][0]] = np.nan
        df[df[col] > value_limits[col][1]] = np.nan

def load_dataset_from_directory_partial(directory, col_of_interest):
    """
    @param directory: directory that stores all the .csv files
           to be considered
    @param col_of_interest: list with containing the names of the
           columns of interest (string)
    @return: pandas DataFrame that contains all the selected data
    """              
    big_df = pd.DataFrame()
    file_cnt = 0
    directory_list = os.listdir(directory)
    for filename in directory_list:
        if filename.endswith(".csv"):
            file_cnt += 1
            file = os.path.join(directory, filename)
            with open(file) as f:
                df_tmp = pd.read_csv(file, sep=';', dtype={'hhmmss': object}, engine='python')[col_of_interest]
                # set all errors to NaN
                df_tmp = df_tmp.applymap(lambda x: contains_error(x))
                # drop every row that contains NaN values
                df_tmp = df_tmp.dropna()
                apply_type_conversion(df_tmp, col_of_interest)
                # set all limit violations to NaN
                apply_limits(df_tmp, col_of_interest)
                # drop every row that contains NaN values
                df_tmp = df_tmp.dropna()
                big_df = pd.concat([big_df, df_tmp], ignore_index=True)
                sys.stdout.write("{} of {}".format(file_cnt, len(directory_list)))
                sys.stdout.write('\r')
    sys.stdout.write('\n')

    return big_df

def load_dataset_from_directory_partial_average_hours(directory, col_of_interest):
    """
    @param directory: directory that stores all the .csv files
           to be considered
    @param col_of_interest: list with containing the names of the
           columns of interest (string)
    @return: pandas DataFrame that contains all the selected data, averaged by hours
    """              
    big_df = pd.DataFrame()
    file_cnt = 0
    directory_list = os.listdir(directory)
    for filename in directory_list:
        if filename.endswith(".csv"):
            file_cnt += 1
            file = os.path.join(directory, filename)
            with open(file) as f:
                df_tmp = pd.read_csv(file, sep=';', dtype={'hhmmss': object}, engine='python')[col_of_interest]
                # set all errors to NaN
                df_tmp = df_tmp.applymap(lambda x: contains_error(x))
                # drop every row that contains NaN values
                df_tmp = df_tmp.dropna()
                apply_type_conversion(df_tmp, col_of_interest)
                # set all limit violations to NaN
                apply_limits(df_tmp, col_of_interest)
                # drop every row that contains NaN values
                df_tmp = df_tmp.dropna()
                # Average over Hours
                add_time_columns(df_tmp)
                df_tmp = df_tmp.groupby(['Hour', 'YYYYMMDD'], as_index=False).mean()
                big_df = pd.concat([big_df, df_tmp], ignore_index=True)
                sys.stdout.write("{} of {}".format(file_cnt, len(directory_list)))
                sys.stdout.write('\r')
    sys.stdout.write('\n')

    return big_df


def load_multiple_datasets_average_hours(direcotries: list, col_of_interest: list):
    """
    @param directories: a list of strings that contains all the directories where
           data is stored
    @param col_of_interest: list with containing the names of the
           columns of interest (string)
    @return: a single pandas DataFrame that contains all the selected data,
             averaged by hours
    """       
    df_ret = pd.DataFrame()
    for d in direcotries:
        df_tmp = load_dataset_from_directory_partial_average_hours(d, col_of_interest)
        df_ret = pd.concat([df_ret, df_tmp])

    return df_ret
