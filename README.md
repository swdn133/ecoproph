# ecoproph
Energy Consumption Prophet - A Machine Learning based Energy Forecast

![logo](/assets/logo.png)

## Reduce the resolution from the dataset from seconds to minutes
This function creates a new folder 'minutes' in the given path and saves
an according .csv for every data file

```
python3 src/reduce_dataset_minutes.py --path R:/ecoproph/Dataset/2018
```

- new file is .csv format
- new file starts with header
- resolution is now minutes

Depending on the number of files this procedure can be pretty time consuming!

## Import Data in Pandas Dataframe
- Import the cleaned .csv Data
- Drop all Rows containing err flags

```python
import sys
sys.path.append('C:\\workspace\\ecoproph\\src\\')
import datasetutils as du

directory = "R:\\ecoproph\\Dataset\\2018\\minutes_2018_new"
col_of_interest = ['unixtimestamp', 'YYYYMMDD', 'hhmmss', 'AEZ-P_SUM']

df = du.load_dataset_from_directory_partial(directory, col_of_interest)

print(df.shape)
```

Plotting the data (after cleaning the error fields) results in the following:

| ![logo](/assets/data16.png) | 
|:---------------------------:|
| Data AEZ-PSUM for 2016      | 

| ![logo](/assets/data17.png) | 
|:---------------------------:|
| Data AEZ-PSUM for 2017      | 

| ![logo](/assets/data18.png) | 
|:---------------------------:|
| Data AEZ-PSUM for 2018      | 


