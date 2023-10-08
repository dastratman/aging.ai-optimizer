# aging.ai-optimizer

## Set up your virtual environment

[How to Set Up a Virtual Environment in Python – And Why It's Useful](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)

```
$ virtualenv --system-site-packages -p python ./venv

$ venv\Scripts\activate.bat

$ pip install
```
## Collecting predictions

Request the aging.ai prediction for a set of biometric data:

```
$ python collect_predictions.py --collect=False --biomarker_data=sample_data/patient_05.json
```

Collect aging.ai predictions for various points across the reference range for a single biomarker, keeping the other biomarkers constant:

```
$ python collect_predictions.py --biomarker_data_filename sample_data/patient_05.json --predictions_directory predictions/patient_05/ --biomarker Albumin
```

Collect predictions for *all* biomarkers, iterating through each one:

```
$ python collect_predictions.py --biomarker_data_filename sample_data/patient_05.json --predictions_directory predictions/patient_05/
```

## Plotting

Generate scatter plots and regressions of the predictions:

```
$ python generate_plots.py --predictions_directory predictions/patient_05/ --plots_directory plots/patient_05/ --biomarker_data_filename sample_data/patient_05.json
```

## Calculating optimal values

Calculate the optimal value for each biomarker for a given set of predictions:

```
$ python optimize.py --predictions_directory predictions/patient_05/
```

Calculate the potential year reduction for each biomarker by achieving the optimal value:

```
$ python optimize.py --calculate_improvement --biomarker_data=sample_data/patient_05.json --optimal_values=sample_data/optimal_patient_05.json
```