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

| ![logo](/assets/data16.png) | ![histo](/assets/histo_16_AEZ-P_SUM__small.png) |
|:---------------------------:|:-----------------------------------------------:|
| Data AEZ-PSUM for 2016      |  Histogram AEZ-PSUM for 2016                    |

| ![logo](/assets/data17.png) | ![histo](/assets/histo_17_AEZ-P_SUM__small.png) |
|:---------------------------:|:-----------------------------------------------:|
| Data AEZ-PSUM for 2017      |  Histogram AEZ-PSUM for 2017                    |

| ![logo](/assets/data18.png) | ![histo](/assets/histo_18_AEZ-P_SUM__small.png) |
|:---------------------------:|:-----------------------------------------------:|
| Data AEZ-PSUM for 2018      |  Histogram AEZ-PSUM for 2018                    |

## Main Functionality
- Load the Datasets
- Create a Regression Model with Facebook Prophet
- Fit the model
- Predit the future
- Plot the prediction and save the plots
    - Prediction and Training Data
    - Regression Components

```
$ cd src
$ python3 ./ecoproph.py
```

will save the created plots in the root folder.

Please adapt the script to your needs. Currently, the Paths to the datasets
and plot outputs are hardcoded absolute paths. This might be resolved in a
later release.

### WIP: Regression Model
The first step is the most primitive fbprophet model available. No tweaks
were made. It's simply the datasets for three years are fit to the primitive 
model and a forecast for a span of a year is done.

### Results
This are the results of the primitive, unoptimized model just at the first shot:

| ![forecast](/assets/forecast__small.png) |
|:----------------------------------------:|
| Facebook Prophet forecast                |


| ![components](/assets/components__small.png) |
|:--------------------------------------------:|
| Plot of the regression components            |

### Validation
Validation is done via Prophet's cross-validation method. For validation,
a saved model has to be provided via a pickle file. 
Validation can be started via the following command:

```
$ cd src
$ python3 ./validation.py
```

The validation script creates an output plot of the MAPE metric
saved as .png file:

| ![components](/assets/validation_small.png)  |
|:--------------------------------------------:|
| Validation via MAPE metric - plot            |

