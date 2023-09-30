import json
import argparse
import copy
from common import request_age
import numpy as np


def calculate_potential_improvement(biomarker, biomarker_data, optimal_data):
    data_copy = copy.copy(biomarker_data)
    data_copy[biomarker] = optimal_data[biomarker]

    print("Calculating new age when optimizing " + biomarker)

    new_predicted_age = request_age(data_copy)
    print("New predicted age: " + str(new_predicted_age))


def calculate_optimal_value(age_predictions, low_end, high_end):
    x_list = [item['value'] for item in age_predictions]
    y_list = [item['predicted_age'] for item in age_predictions]

    x = np.array(x_list)
    y = np.array(y_list)

    # 2nd degree linear regression
    coef2 = np.polyfit(x, y, 2)

    # Create a list of 100 input values
    x_calc = list(np.arange(low_end, high_end, (high_end - low_end) / 100))
    # Calculate the result of input values
    y_calc = np.polyval(coef2, x_calc)

    # Return the input value which results in the lowest age
    index_of_lowest_value = np.argmin(y_calc)
    return round(x_calc[index_of_lowest_value], 2)


def calculate_optimal_values(biomarker_ranges, predictions_directory):
    print('Calculating optimal values for biomarkers')
    optimal_values = []

    for biomarker_range in biomarker_ranges:
        biomarker = biomarker_range['biomarker']
        low_end = biomarker_range['low_end']
        high_end = biomarker_range['high_end']

        age_predictions = []
        with open(predictions_directory + biomarker + ".json",
                  'r') as json_file:
            age_predictions = json.load(json_file)

        optimal_value = calculate_optimal_value(age_predictions, low_end,
                                                high_end)

        optimal_values.append({
            biomarker: optimal_value,
        })

    print(optimal_values)


def main():
    parser = argparse.ArgumentParser(
        description="Collect predictions from Aging.ai.")

    # Define a flag
    parser.add_argument("--biomarker_data_filename",
                        help="filename with comparison biomarker data values",
                        default="sample_data/patient_05.json")

    parser.add_argument("--optimal_values_filename",
                        help="filename with optimal biomarker data values",
                        default="sample_data/optimal_patient_05.json")

    parser.add_argument("--metric_ranges_filename",
                        help="filename with acceptable metric ranges",
                        default="metric_ranges.json")

    parser.add_argument("--predictions_directory",
                        help="directory to store aging.ai age predictions",
                        default="predictions/temp/")

    parser.add_argument("--biomarker",
                        help="only compare a specific biomarker")

    parser.add_argument("--calculate_optimal_values",
                        help="whether to calculate optimal values",
                        action="store_true",
                        default=True)

    parser.add_argument("--calculate_improvement",
                        help="whether to calculate optimal values",
                        action="store_true",
                        default=False)

    args = parser.parse_args()

    with open(args.metric_ranges_filename, 'r') as json_file:
        print('Reading metric ranges from ' + args.metric_ranges_filename)
        biomarker_ranges = json.load(json_file)

    print('')

    if args.calculate_optimal_values and not args.calculate_improvement:
        calculate_optimal_values(biomarker_ranges, args.predictions_directory)

    if args.calculate_improvement:
        with open(args.biomarker_data_filename, 'r') as json_file:
            print('Reading control biomarker data from ' +
                  args.biomarker_data_filename)
            biomarker_data = json.load(json_file)

        with open(args.optimal_values_filename, 'r') as json_file:
            print('Reading optimal biomarker data from ' +
                  args.optimal_values_filename)
            optimal_data = json.load(json_file)

        if args.biomarker:
            calculate_potential_improvement(args.biomarker, biomarker_data,
                                            optimal_data)
        else:
            print("\nCalculating original age")
            original_predicted_age = request_age(biomarker_data)
            print("Original predicted age: " + str(original_predicted_age))
            for biomarker_range in biomarker_ranges:
                biomarker = biomarker_range['biomarker']
                calculate_potential_improvement(biomarker, biomarker_data,
                                                optimal_data)


if __name__ == "__main__":
    main()