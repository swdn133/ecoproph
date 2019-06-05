import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from fbprophet import Prophet
import pickle


import datasetutils as du
import holidays_hm

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

    return prophet_df


def convert_timestamp_to_string(unixtime):
    """
    @param unixtime: unixtimestamp that you want the string of
    @return: formatted string representation of given unixtime
    """              
    return datetime.utcfromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')


def plot_forecast(df, ts_start, ts_stop, label=''):
    """
    @param df: forecast dataframe
    @param ts_start: start time of the plot
    @param ts_stop: end time of the plot
    """   
    # retreive the selected data
    df['ds'] = pd.to_datetime(df['ds'])
    df = df.set_index(['ds'])
    df = df.loc[ts_start:ts_stop]
    df = df.reset_index()

    # plot it
    plt.figure()
    plt.plot(df['ds'], df['yhat'], color='blue')
    plt.plot(df['ds'], df['yhat_lower'], color='lightblue')
    plt.plot(df['ds'], df['yhat_upper'], color='lightblue')
    plt.xlim((df['ds'].iloc[0], df['ds'].iloc[-1]))
    plt.title('Forecast ' + label + ' from ' + ts_start + ' to ' + ts_stop)
    plt.ylabel('R_BauTGb-P_SUM [kW]')
    plt.xlabel('Date')
    plt.xticks(rotation=25)
    plt.fill_between(df['ds'], df['yhat_lower'], df['yhat_upper'], color='lightblue')
    

def main():
    # select and load the data
    col_of_interest = ['unixtimestamp', 'YYYYMMDD', 'hhmmss', 'AEZ-P_SUM',
                       'R_BauBGa-P_SUM', 'R_BauBGb-P_SUM', 'R_BauTGb-P_SUM']

    directory18 = "R:\\ecoproph\\Messdaten_HM\\2018\\minutes_2018_new"
    directory17 = "R:\\ecoproph\\Messdaten_HM\\2017\\minutes_2017_new"
    directory16 = "R:\\ecoproph\\Messdaten_HM\\2016\\minutes_2016_new\\2016_newcol"



    # creating and fitting the model
    try:
        print("Try to read model parameters...")
        with open('C:\\workspace\\ecoproph\\ecoproph.pckl', 'rb') as fin:
            model = pickle.load(fin)
        print("... Success")
    except FileNotFoundError:
        print("No saved .pckl model found! Creating new model...")
        print("loading datasets...")
        start = datetime.now()
        df = du.load_multiple_datasets_average_hours([directory16, directory17, directory18],
                                                     col_of_interest)

        print("Time elapsed [seconds]: ", (datetime.now() - start).total_seconds())
        prophet_df = build_prophet_dataframe(df, 'R_BauTGb-P_SUM')
        df_holidays = holidays_hm.get_holidays_dataframe()
        model = Prophet(yearly_seasonality=6, weekly_seasonality=40, daily_seasonality=10, 
                    holidays=df_holidays, holidays_prior_scale=80, 
                    seasonality_prior_scale=100, changepoint_prior_scale=0.0001)
        print("Model fitting...")
        start = datetime.now()
        model.fit(prophet_df)
        print("Time elapsed [seconds]: ", (datetime.now() - start).total_seconds())
        with open('C:\\workspace\\ecoproph\\ecoproph.pckl', 'wb') as fout:
            pickle.dump(model, fout)

    # Predicting the future
    future = model.make_future_dataframe(periods=365*24, freq='H')
    print("Predict future for 365 days...")
    start = datetime.now()
    forecast = model.predict(future)
    print("Time elapsed [seconds]: ", (datetime.now() - start).total_seconds())

    print("plotting")
    model.plot(forecast)
    plt.savefig('C:\\workspace\\ecoproph\\forecast.png', bbox_inches='tight', dpi=500)

    model.plot_components(forecast)
    plt.savefig('C:\\workspace\\ecoproph\\components.png', bbox_inches='tight', dpi=500)
    
    plot_forecast(forecast, '2019-02-04', '2019-03-13', 'R_BauTGb-P_SUM')
    plt.savefig('C:\\workspace\\ecoproph\\my_plot.png', bbox_inches='tight', dpi=500)

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

