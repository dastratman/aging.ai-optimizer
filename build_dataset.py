from common import request_age
import argparse
import csv
import json
import random


def find_biomarker_range(biomarker_ranges, key, value):
    for d in biomarker_ranges:
        if key in d and d[key] == value:
            return d
    return None


def generate_input(biomarker_ranges):
    input_biomarker_data = {
        "Albumin": "0",
        "Glucose": "0",
        "Urea": "0",
        "Cholesterol": "0",
        "Protein_total": "0",
        "Sodium": "0",
        "Creatinine": "0",
        "Hemoglobin": "0",
        "Bilirubin_total": "0",
        "Triglycerides": "0",
        "HDL_Cholesterol": "0",
        "LDL_cholesterol": "0",
        "Calcium": "0",
        "Potassium": "0",
        "Hematocrit": "0",
        "MCHC": "0",
        "MCV": "0",
        "Platelets": "0",
        "Erythrocytes": "0"
    }

    for key, value in input_biomarker_data.items():
        input_biomarker_data[key] = round(
            random.uniform(biomarker_ranges[key]['low_end'],
                           biomarker_ranges[key]['high_end']), 2)

    input_biomarker_data.update({
        "ethnicity":
        "western_europe",
        "metric":
        "us",
        "weight":
        "190",
        "height":
        "72",
        "smoke":
        "no",
        "csrfmiddlewaretoken":
        "4SdAofEdCaohTw7FZ2uHprZ7z4GAHhRZ",
    })

    return input_biomarker_data


def write_array_of_dicts_to_csv(array_of_dicts, output_filename):
    # Extract field names (keys) from the first dictionary in the list
    fieldnames = array_of_dicts[0].keys()

    # Open the CSV file for writing
    with open(output_filename, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the header (field names)
        writer.writeheader()

        # Write the rows
        for row in array_of_dicts:
            writer.writerow(row)


def generate_datapoint(dataset_filename, biomarker_ranges):
    predictions = []

    for x in range(1000):
        print('\n### Iteration ' + str(x) + ' ###\n')

        # Generate random data within reference ranges
        biomarker_data = generate_input(biomarker_ranges)
        print(biomarker_data)

        # Request predicted age
        predicted_age = request_age(biomarker_data)
        biomarker_data['predicted_age'] = predicted_age
        print("Prediction age: " + str(predicted_age))

        # Write all results to file
        del biomarker_data['csrfmiddlewaretoken']
        predictions.append(biomarker_data)
        write_array_of_dicts_to_csv(predictions, dataset_filename)


def main():
    parser = argparse.ArgumentParser(
        description="Collect predictions from Aging.ai.")

    # Define a flag
    parser.add_argument("--dataset_filename",
                        help="filename to save dataset",
                        default="sample_data/aging.ai-dataset.csv")

    parser.add_argument("--metric_ranges_filename",
                        help="filename with acceptable metric ranges",
                        default="metric_ranges.json")

    args = parser.parse_args()

    biomarker_ranges = []

    with open(args.metric_ranges_filename, 'r') as json_file:
        print('Reading metric ranges from ' + args.metric_ranges_filename)
        biomarker_ranges = json.load(json_file)

    biomarker_ranges = {d['biomarker']: d for d in biomarker_ranges}

    generate_datapoint(args.dataset_filename, biomarker_ranges)


if __name__ == "__main__":
    main()