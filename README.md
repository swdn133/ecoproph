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

