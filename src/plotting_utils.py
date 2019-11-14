import pickle
import pandas as pd
import matplotlib.pyplot as plt

def apply_day_column(df):
    timestamp_col = df['ds']
    newcol = timestamp_col.apply(lambda x: x.day).rename('day')
    df['day'] = newcol

    return df


def sum_a_day(df, ts_start, ts_stop):
    df['ds'] = pd.to_datetime(df['ds'])
    df = df.set_index(['ds'])
    df = df.loc[ts_start:ts_stop]
    df = df.reset_index()
    df_temp = df.groupby(['day'], as_index=False).sum(axis=0)

    return df_temp


def load_forecast_dataframe(path: str):
    with open(path, 'rb') as fin:
        forecast_df = pickle.load(fin)
    return forecast_df


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


def plot_month_forecast_bar(df, label):
    plt.figure()
    plt.step(df['day'], df['yhat'], color='blue')
    plt.step(df['day'], df['yhat_lower'], color='lightblue')
    plt.step(df['day'], df['yhat_upper'], color='lightblue')
    plt.xlim((df['day'].iloc[0], df['day'].iloc[-1]))
    plt.title('Forecast ' + label)
    plt.ylabel('R_BauTGb-P_SUM [kW]')
    plt.xlabel('Date')
    plt.xticks(rotation=25)



if __name__ == '__main__':
    forecast = load_forecast_dataframe("C:\workspace\ecoprophet\forecast.pckl")

    forecast = apply_day_column(forecast)

    df = sum_a_day(forecast, '2019-09-01', '2019-09-30')
    plot_month_forecast(df, 'september')
    plt.show()
