import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from fbprophet import Prophet


import datasetutils as du


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


def main():
    col_of_interest = ['unixtimestamp', 'YYYYMMDD', 'hhmmss', 'AEZ-P_SUM',
                       'R_BauBGa-P_SUM', 'R_BauBGb-P_SUM']

    directory18 = "R:\\ecoproph\\Messdaten_HM\\2018\\minutes_2018_new"
    directory17 = "R:\\ecoproph\\Messdaten_HM\\2017\\minutes_2017_new"
    directory16 = "R:\\ecoproph\\Messdaten_HM\\2016\\minutes_2016_new\\2016_newcol"

    print("loading datasets...")
    df = du.load_multiple_datasets_average_hours([directory16, directory17, directory18],
                                                 col_of_interest)

    prophet_df = build_prophet_dataframe(df, 'AEZ-P_SUM')

    model = Prophet()
    print("Model fitting...")
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=365)
    print("Predict future for 365 days...")
    forecast = model.predict(future)

    print("plotting")
    model.plot(forecast)
    plt.savefig('C:\\workspace\\ecoproph\\forecast.png', bbox_inches='tight', dpi=500)

    model.plot_components(forecast)
    plt.savefig('C:\\workspace\\ecoproph\\components.png', bbox_inches='tight', dpi=500)
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

