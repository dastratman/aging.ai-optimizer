import time
import copy
import json
import numpy as np
import argparse
from common import request_age


def save_predictions(biomarker, age_predictions):
    with open("predictions/" + biomarker + ".json", "w") as file:
        json.dump(age_predictions, file)


def collect_predictions(biomarker, biomarker_range, step_count,
                        biomarker_data):

    low_end = biomarker_range['low_end']
    high_end = biomarker_range['high_end']

    # Evenly divide the reference range based on the number of steps
    step = (high_end - low_end) / step_count

    age_predictions = []
    data_copy = copy.copy(biomarker_data)

    for i in np.arange(low_end, high_end + step, step):
        i = round(i, 2)
        data_copy[biomarker] = i

        print("Calculating " + biomarker + " of " + str(i))

        # Request predicted age
        predicted_age = request_age(data_copy)

        print("Prediction age: " + str(predicted_age))
        age_predictions.append({
            "biomarker": biomarker,
            "value": i,
            "predicted_age": predicted_age
        })

        time.sleep(3)

    print("\n### Finished calculations for " + biomarker + " ###\n")

    # Once all samples have been collected for a biomarker, save to a file
    save_predictions(biomarker, age_predictions)


def main():
    parser = argparse.ArgumentParser(
        description="Collect predictions from Aging.ai.")

    # Define a flag
    parser.add_argument("--step_count",
                        help="number of evenly spaced samples to collect",
                        default="20")

    parser.add_argument(
        "--biomarker_data",
        help="filename with biomarker data values for collection iteration",
        default="configs/sample_patient_05.json")

    parser.add_argument("--metric_ranges",
                        help="filename with acceptable metric ranges",
                        default="configs/metric_ranges.json")

    parser.add_argument("--collect",
                        help="filename with acceptable metric ranges",
                        default=True)

    parser.add_argument("--biomarker",
                        help="only collect a specific biomarker")

    args = parser.parse_args()

    with open(args.biomarker_data, 'r') as json_file:
        print('Reading biomarker data from ' + args.biomarker_data)
        biomarker_data = json.load(json_file)

    print('')

    if args.collect == True:
        with open(args.metric_ranges, 'r') as json_file:
            print('Reading metric ranges from ' + args.metric_ranges)
            biomarker_ranges = json.load(json_file)

        step_count = int(args.step_count)

        if args.biomarker:
            biomarker_range = [
                item for item in biomarker_ranges
                if item['biomarker'] == args.biomarker
            ]

            collect_predictions(args.biomarker, biomarker_range[0], step_count,
                                biomarker_data)
        else:
            for biomarker_range in biomarker_ranges:
                biomarker = biomarker_range['biomarker']

                collect_predictions(biomarker, biomarker_range, step_count,
                                    biomarker_data)
    else:
        predicted_age = request_age(biomarker_data)
        print('Predicted age: ' + str(predicted_age))


if __name__ == "__main__":
    main()