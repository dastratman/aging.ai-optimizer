# aging.ai-optimizer

Request the aging.ai prediction for a set of biometric data:

```
$ python collect_predictions.py --collect=False --biomarker_data=sample_data/dastratman.json
```

Collect aging.ai predictions for various points across the reference range for a single biomarker, keeping the other biomarkers constant:

```
$ python collect_predictions.py --biomarker_data_filename sample_data/patient_05.json --predictions_directory predictions/sample_patient_05/ --biomarker Albumin
```

Collect predictions for *all* biomarkers, iterating through each one:

```
$ python collect_predictions.py --biomarker_data_filename sample_data/patient_05.json --predictions_directory predictions/sample_patient_05/
```

Generate scatter plots and regressions of the predictions:

```

```

Calculate the optimal value for each biomarker for a given set of predictions:

```

```

Calculate the potential year reduction for each biomarker by achieving the optimal value:

```
$ python optimize.py --calculate_improvement --biomarker_data=sample_data/dastratman.json --optimal_values=sample_data/optimal_dastratman.json
```