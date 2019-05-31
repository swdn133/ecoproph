import pandas as pd

free_holidays = pd.DataFrame({
    'holiday': 'free_holiday',
    'ds': pd.to_datetime(['2016-01-01', '2016-01-06', '2016-03-27',
                          '2016-05-15', '2016-12-25', '2016-12-26',
                          '2017-01-01', '2017-01-06', '2017-04-16',
                          '2017-06-04', '2017-12-25', '2017-12-26',
                          '2018-01-01', '2018-01-06', '2018-04-01',
                          '2018-05-20', '2018-12-25', '2018-12-26',
                          '2019-01-01', '2019-01-06', '2019-04-21',
                          '2019-06-09', '2019-12-25', '2019-12-26',
                          '2020-01-01', '2020-01-06', '2020-04-12',
                          '2020-05-31', '2020-12-25', '2020-12-26',                            
    ]),
    'lower_window': -3,
    'upper_window': 3
})

exams = pd.DataFrame({
    'holiday': 'exam',
    'ds': pd.to_datetime(['2016-01-25', '2016-07-11', 
                          '2017-01-25', '2017-07-11', 
                          '2018-01-25', '2018-07-11', 
                          '2019-01-25', '2019-07-11', 
                          '2020-01-25', '2020-07-11',                        
        
    ]),
    'lower_window': -3,
    'upper_window': 15
})

free_summer = pd.DataFrame({
    'holiday': 'free_summer',
    'ds': pd.to_datetime(['2015-10-01', '2016-10-01', '2017-10-01',
                          '2018-10-01', '2019-10-01', '2020-10-01'
        
    ]),
    'lower_window': -70,
    'upper_window': 2    
})

free_winter = pd.DataFrame({
    'holiday': 'free_winter',
    'ds': pd.to_datetime(['2015-03-15', '2016-03-15', '2017-03-15',
                          '2018-03-15', '2019-03-15', '2020-03-15'
        
    ]),
    'lower_window': -40,
    'upper_window': 2    
})

def get_holidays_dataframe():
  return pd.concat([free_holidays, exams, free_summer, free_winter])