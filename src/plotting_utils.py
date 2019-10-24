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


def plot_month_forecast(df, label):
    plt.figure()
    plt.step(df['day'], df['yhat'], color='blue')
    plt.step(df['day'], df['yhat_lower'], color='lightblue')
    plt.step(df['day'], df['yhat_upper'], color='lightblue')
    plt.xlim((df['day'].iloc[0], df['day'].iloc[-1]))
    plt.title('Forecast ' + label)
    plt.ylabel('R_BauTGb-P_SUM [kW]')
    plt.xlabel('Date')
    plt.xticks(rotation=25)




with open('C:\\workspace\\ecoproph\\forecast.pckl', 'rb') as fin:
    forecast = pickle.load(fin)

forecast = apply_day_column(forecast)

df = sum_a_day(forecast, '2019-09-01', '2019-09-30')
plot_month_forecast(df, 'september')
plt.show()
