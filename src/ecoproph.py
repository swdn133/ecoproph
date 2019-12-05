import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from fbprophet import Prophet
import pickle


import datasetutils as du
import dwd_utils
import holidays_hm
import plotting_utils

def build_prophet_dataframe_sum(input_data, value_columns: list):
    prophet_df = pd.DataFrame()
    input_data['timestring'] = input_data['unixtimestamp'].apply(
        lambda x: convert_timestamp_to_string(x))
    prophet_df['ds'] = input_data['timestring']
    prophet_df['y'] = input_data[value_columns].sum(axis=1)
    prophet_df['temp'] = input_data['TT_TU']

    return prophet_df


def build_prophet_dataframe(input_data, value_column):
    """
    @param imput_data: pandas dataframe that contains the values
           relevant for the prophet model as well as a unixtimestamp
    @param col_of_interest: name of the interested data column
    @return: pandas DataFrame used for fbprophet fitting
    """          
    prophet_df = pd.DataFrame()

    # define a new column timestring that contains the string
    # converted from utc timestamp (string format defined by
    # facebook prophet)
    input_data['timestring'] = input_data['unixtimestamp'].apply(
        lambda x: convert_timestamp_to_string(x))
    prophet_df['ds'] = input_data['timestring']
    prophet_df['y'] = input_data[value_column]
    prophet_df['temp'] = input_data['TT_TU']

    return prophet_df


def convert_timestamp_to_string(unixtime):
    """
    @param unixtime: unixtimestamp that you want the string of
    @return: formatted string representation of given unixtime
    """              
    # TODO: 29:30 is because of the mean() that is applied to the
    # timestamp during dataset preprocessing
    return datetime.utcfromtimestamp(unixtime).strftime('%Y-%m-%d %H:29:30')


def get_temperature(x, dwd_df):
    timestring = x.strftime("%Y-%m-%d %H:%M:%S")
    return dwd_df.loc[timestring]['TT_TU']


def main():
    # select and load the data
    """
    col_of_interest = ['unixtimestamp', 'YYYYMMDD', 'hhmmss', 'AEZ-P_SUM',
                       'R_BauBGa-P_SUM', 'R_BauBGb-P_SUM', 'R_Bau_TGa-P_SUM', 'R_BauTGb-P_SUM', 
                       'E_BauXa-P_SUM', 'E_BauXb-P_SUM']
    """
    col_of_interest = ['unixtimestamp', 'YYYYMMDD', 'hhmmss', 
                       'PV_120kW-P_SUM']
    power_sum = ['AEZ-P_SUM',
                 'R_BauBGa-P_SUM', 'R_BauBGb-P_SUM', 'R_Bau_TGa-P_SUM', 'R_BauTGb-P_SUM', 
                 'E_BauXa-P_SUM', 'E_BauXb-P_SUM']

    directory18 = "R:\\ecoproph\\Messdaten_HM\\2018\\minutes_2018_new"
    directory17 = "R:\\ecoproph\\Messdaten_HM\\2017\\minutes_2017_new"
    directory16 = "R:\\ecoproph\\Messdaten_HM\\2016\\minutes_2016_new\\2016_newcol"

    # load data of historical ambient temperature from dwd
    dwd_df = dwd_utils.load_dwd_dataframe('C:/workspace/produkt_tu_stunde_19920517_20181231_01262.txt')
    dwd_df = dwd_utils.prepare_tt_tu_dataframe(dwd_df, '20170101')

    # creating and fitting the model
    try:
        print("Try to read model parameters...")
        with open('C:\\workspace\\ecoproph\\ecoproph_experimentalPvModelA100.pckl', 'rb') as fin:
            model = pickle.load(fin)
        print("... Success")
    except FileNotFoundError:
        print("No saved .pckl model found! Creating new model...")
        print("loading datasets...")
        start = datetime.now()
        df = du.load_multiple_datasets_average_hours([directory17, directory18],
                                                     col_of_interest)

        df = pd.merge(df, dwd_df, how='left', on=['YYYYMMDD', 'Hour'])
        
        print("Time elapsed [seconds]: ", (datetime.now() - start).total_seconds())
        #prophet_df = build_prophet_dataframe_sum(df, power_sum)
        prophet_df = build_prophet_dataframe(df, 'PV_120kW-P_SUM')
        df_holidays = holidays_hm.get_holidays_dataframe()
        model = Prophet(yearly_seasonality=6, weekly_seasonality=False, daily_seasonality=20, 
                    # holidays=df_holidays, holidays_prior_scale=80 ,
                    seasonality_prior_scale=100, changepoint_prior_scale=0.0001)
        model.add_regressor('temp', mode="additive", standardize=False, prior_scale=100)
        print("Model fitting...")
        start = datetime.now()
        model.fit(prophet_df)
        print("Time elapsed [seconds]: ", (datetime.now() - start).total_seconds())
        with open('C:\\workspace\\ecoproph\\ecoproph_experimentalPvModelA100.pckl', 'wb') as fout:
            pickle.dump(model, fout)
            print("Saved fitted model")

    # Predicting the future
    future_dwd = dwd_utils.load_dwd_dataframe('C:/workspace/produkt_tu_stunde_20180529_20191129_01262.txt')
    future_dwd = dwd_utils.prepare_tt_tu_dataframe(future_dwd, '20190101')
    dwd_df = dwd_df.append(future_dwd)
    dwd_df = dwd_df.set_index(['timestring'])

    future = model.make_future_dataframe(periods=300*24, freq='H')
    future['temp'] = future['ds'].apply(lambda x: get_temperature(x, dwd_df))
    dwd_df = dwd_df.reset_index()
    print("Predict future for 365 days...")
    start = datetime.now()
    forecast = model.predict(future)

    with open('C:\\workspace\\ecoproph\\forecast_experimentalPvModelA100.pckl', 'wb') as fout:
        pickle.dump(forecast, fout)
        print('Saved forecast')

    print("Time elapsed [seconds]: ", (datetime.now() - start).total_seconds())

    print("plotting")
    model.plot(forecast)
    plt.savefig('C:\\workspace\\ecoproph\\forecast.png', bbox_inches='tight', dpi=500)

    model.plot_components(forecast)
    plt.savefig('C:\\workspace\\ecoproph\\components.png', bbox_inches='tight', dpi=500)
    
    # plotting_utils.plot_forecast(forecast, '2019-09-01', '2019-09-30', 'R_BauTGb-P_SUM')
    # plt.savefig('C:\\workspace\\ecoproph\\my_plot.png', bbox_inches='tight', dpi=500)

    plt.show()

if __name__ == '__main__':
    splash = """\n\n
 _____ _____ _________________ ___________ _   _ 
|  ___/  __ \  _  | ___ \ ___ \  _  | ___ \ | | |
| |__ | /  \/ | | | |_/ / |_/ / | | | |_/ / |_| |
|  __|| |   | | | |  __/|    /| | | |  __/|  _  |
| |___| \__/\ \_/ / |   | |\ \\  \_/ / |   | | | |
\____/ \____/\___/\_|   \_| \_|\___/\_|   \_| |_/                                            
    \n\n"""
    print(splash)
    main()

