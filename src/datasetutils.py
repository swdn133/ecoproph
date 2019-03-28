import numpy as np
import os
import pandas as pd
import sys


def contains_error(val):    
    """
    @param val: the value you want to check for errors
    @return: if no error: input, if error: NaN
    """
    if 'err' in "{}".format(val):
        return np.nan
    else:
        return val


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
                df_tmp = pd.read_csv(file, sep=';', engine='python')[col_of_interest]
                # set all errors to NaN
                df_tmp = df_tmp.applymap(lambda x: contains_error(x))
                # drop every row that contains NaN values
                df_tmp = df_tmp.dropna()
                big_df = pd.concat([big_df, df_tmp], ignore_index=True)
                sys.stdout.write("{} of {}".format(file_cnt, len(directory_list)))
                sys.stdout.write('\r')
    sys.stdout.write('\n')

    return big_df
