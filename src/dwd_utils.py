import pandas as pd
import numpy as np
import datetime

def load_dwd_dataframe(path: str):
    """
    @param ts_start: path to dwd data (csv formatted file)
    @return: pandas DataFrame for entire dwd data
    """      
    df = pd.read_csv(path, sep=';')
    return df


def prepare_tt_tu_dataframe(df, ts_start: str):
    """
    @param df: pandas dataframe that contains the entire
               historical dwd data for TT_TU (ambient temperature)
    @param ts_start: string containing the start date YYYYMMDD
    @return: pandas DataFrame containing TT_TU, YYYYMMDD, Hour
    """           
    df_r = df.set_index(['MESS_DATUM'])
    df_r = df_r.loc[ts_start:]
    df_r = df_r.reset_index()
    df_r['YYYYMMDD'] = df_r['MESS_DATUM'].astype(str)
    df_r['Hour'] = df_r['YYYYMMDD'].str[8:10].astype(np.float64)
    df_r['YYYYMMDD'] = df_r['YYYYMMDD'].str[:8]  # only date, not hour
    # drop all the unneccessary columns
    df_r['timestring'] = df_r['MESS_DATUM'].astype(str).apply(create_timestring)
    df_r = df_r.drop(['STATIONS_ID', 'QN_9', 'eor', 'RF_TU', 'MESS_DATUM'], axis=1)
    
    return df_r


def prepare_sd_so_dataframe(df, ts_start: str):
    """
    @param df: pandas dataframe that contains the entire
               historical dwd data for SD_SO (hours of sunshine)
    @param ts_start: string containing the start date YYYYMMDD
    @return: pandas DataFrame containing SD_SO, YYYYMMDD, Hour
    """           
    df_r = df.set_index(['MESS_DATUM'])
    df_r = df_r.loc[ts_start:]
    df_r = df_r.reset_index()
    df_r['YYYYMMDD'] = df_r['MESS_DATUM'].astype(str)
    df_r['Hour'] = df_r['YYYYMMDD'].str[8:10].astype(np.float64)
    df_r['YYYYMMDD'] = df_r['YYYYMMDD'].str[:8]  # only date, not hour
    # drop all the unneccessary columns
    df_r['timestring'] = df_r['MESS_DATUM'].astype(str).apply(create_timestring)
    df_r = df_r.drop(['STATIONS_ID', 'QN_7', 'eor', 'MESS_DATUM'], axis=1)
    
    return df_r


def create_timestring(val):
    time = datetime.datetime(year=int(val[0:4]),
                             month=int(val[4:6]),
                             day=int(val[6:8]),
                             hour=int(val[8:10])
                             )
    time -= datetime.timedelta(seconds=30, minutes=30)
    return time.strftime("%Y-%m-%d %H:%M:%S")