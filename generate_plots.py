import json
import os
import numpy as np
import matplotlib.pyplot as plt
import argparse
from common import request_age


def calculate_coefficient_of_determination(x, y, degree):
    # Compute the coefficients of the linear regression model
    coef = np.polyfit(x, y, degree)

    # Predict y values using the linear model
    y_pred = np.polyval(coef, x)

    # Calculate SSres
    SS_res = np.sum((y - y_pred)**2)

    # Calculate SStot
    SS_tot = np.sum((y - np.mean(y))**2)

    # Calculate R-squared
    r2 = 1 - (SS_res / SS_tot)

    #print(f"R-squared: {r2}")
    return r2


def calculate_regression(biomarker, show_plot, save_plot,
                         predictions_directory, plots_directory,
                         biomarker_data, predicted_age):
    print('\nPlotting ' + biomarker)

    age_predictions = []
    with open(predictions_directory + biomarker + ".json", 'r') as json_file:
        age_predictions = json.load(json_file)

    # Create arrays containing biometric values
    print(biomarker_data[biomarker])
    x_b = np.array([[float(biomarker_data[biomarker])]])
    y_b = np.array([[predicted_age]])

    # Create arrays containing prediction values
    x_list = [item['value'] for item in age_predictions]
    y_list = [item['predicted_age'] for item in age_predictions]

    x = np.array(x_list)
    y = np.array(y_list)

    # Fit 2nd degree polynomial
    coef2 = np.polyfit(x, y, 2)
    y_pred2 = np.polyval(coef2, x)
    rr2 = round(calculate_coefficient_of_determination(x, y, 2), 2)

    # Plot the prediction data
    plt.scatter(x, y, color='blue', label='Predictions')

    # Plot the polynomial regression lines
    eq2 = f'y = {coef2[0]:.2f}x^2 + {coef2[1]:.2f}x + {coef2[2]:.2f}'
    plt.plot(x, y_pred2, color='green', label=f'Equation: {eq2} | RR: {rr2}')

    # Plot the biometric data
    plt.scatter(x_b, y_b, color='red', label='Actual')

    print(f'Equation: {eq2}')
    print(f'RR: {rr2}')

    # Add a title to the plot
    plt.title(biomarker)

    # Add a legend
    plt.xlabel('Biomarker Value')
    plt.ylabel('Predicted Age')
    plt.legend()

    # Add a grid
    plt.grid(True)

    if show_plot:
        plt.show()
    if save_plot:
        # Save the plot to an image file with 300 DPI
        plt.savefig(plots_directory + biomarker + '.png', dpi=300)

    plt.close('all')


def generate_all_plots(show_plot, save_plot, predictions_directory,
                       plots_directory, biomarker_data, predicted_age):
    for filename in os.listdir(predictions_directory):
        if filename.endswith('.json'):
            biomarker = filename.replace('.json', '')
            calculate_regression(biomarker, show_plot, save_plot,
                                 predictions_directory, plots_directory,
                                 biomarker_data, predicted_age)


def main():
    parser = argparse.ArgumentParser(
        description=
        "Calculates regressions based on sample data and generates plots.")

    # Define a flag
    parser.add_argument("--save_plot",
                        help="save plot images",
                        action="store_true",
                        default=True)

    parser.add_argument("--show_plot",
                        help="save plot images",
                        action="store_true",
                        default=False)

    parser.add_argument(
        "--biomarker_data_filename",
        help="filename with biomarker data values for collection iteration",
        default="sample_data/patient_05.json")

    parser.add_argument("--predictions_directory",
                        help="directory to store aging.ai age predictions",
                        default="predictions/patient_05/")

    parser.add_argument("--plots_directory",
                        help="directory to store biomarker plots",
                        default="plots/patient_05/")

    parser.add_argument("--biomarker", help="only plot a specific biomarker")

    args = parser.parse_args()

    with open(args.biomarker_data_filename, 'r') as json_file:
        print('Reading biomarker data from ' + args.biomarker_data_filename)
        biomarker_data = json.load(json_file)

    predicted_age = request_age(biomarker_data)

    if args.biomarker:
        calculate_regression(args.biomarker, args.show_plot, args.save_plot,
                             args.predictions_directory, args.plots_directory,
                             biomarker_data, predicted_age)
    else:
        generate_all_plots(args.show_plot, args.save_plot,
                           args.predictions_directory, args.plots_directory,
                           biomarker_data, predicted_age)


if __name__ == "__main__":
    main()