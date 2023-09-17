import json
import os
import numpy as np
import matplotlib.pyplot as plt
import argparse


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


def calculate_regression(biomarker, show_plot, save_plot):
    print('\nPlotting ' + biomarker)

    age_predictions = []
    with open("predictions/" + biomarker + ".json", 'r') as json_file:
        age_predictions = json.load(json_file)

    x_list = [item['value'] for item in age_predictions]
    y_list = [item['predicted_age'] for item in age_predictions]

    x = np.array(x_list)
    y = np.array(y_list)

    coef1 = np.polyfit(x, y, 1)
    y_pred1 = np.polyval(coef1, x)
    rr1 = round(calculate_coefficient_of_determination(x, y, 1), 2)

    # Fit 2nd degree polynomial
    coef2 = np.polyfit(x, y, 2)
    y_pred2 = np.polyval(coef2, x)
    rr2 = round(calculate_coefficient_of_determination(x, y, 2), 2)

    # Fit 3rd degree polynomial
    coef3 = np.polyfit(x, y, 3)
    y_pred3 = np.polyval(coef3, x)
    rr3 = round(calculate_coefficient_of_determination(x, y, 3), 2)

    # Plot the data
    plt.scatter(x, y, color='blue', label='Data points')

    # Plot the polynomial regression lines
    eq1 = f'y = {coef1[0]:.2f}x + {coef1[1]:.2f}'
    eq2 = f'y = {coef2[0]:.2f}x^2 + {coef2[1]:.2f}x + {coef2[2]:.2f}'
    eq3 = f'y = {coef3[0]:.2f}x^3 + {coef3[1]:.2f}x^2 + {coef3[2]:.2f}x + {coef3[3]:.2f}'

    plt.plot(x, y_pred1, color='red', label=f'1st Degree: {eq1} | RR: {rr1}')
    plt.plot(x, y_pred2, color='green', label=f'2nd Degree: {eq2} | RR: {rr2}')
    plt.plot(x,
             y_pred3,
             color='purple',
             label=f'3rd Degree: {eq3} | RR: {rr3}')

    print(f'1st Degree: {eq1}')
    print(f'RR: {rr1}')

    print(f'2nd Degree: {eq2}')
    print(f'RR: {rr2}')

    print(f'3rd Degree: {eq3}')
    print(f'RR: {rr3}')

    # Add a title to the plot
    plt.title(biomarker)
    plt.legend()
    plt.grid(True)

    if show_plot:
        plt.show()
    if save_plot:
        # Save the plot to an image file with 300 DPI
        plt.savefig('plots/' + biomarker + '.png', dpi=300)

    plt.close('all')


def generate_all_plots(show_plot, save_plot):
    for filename in os.listdir("predictions"):
        if filename.endswith('.json'):
            biomarker = filename.replace('.json', '')
            calculate_regression(biomarker, show_plot, save_plot)


def main():
    parser = argparse.ArgumentParser(
        description=
        "Calculates regressions based on sample data and generates plots.")

    # Define a flag
    parser.add_argument("--save_plot",
                        help="save plot images",
                        action="store_true")

    parser.add_argument("--show_plot",
                        help="save plot images",
                        action="store_true")

    parser.add_argument("--biomarker", help="only plot a specific biomarker")

    args = parser.parse_args()

    if args.biomarker:
        calculate_regression(
            args.biomarker,
            show_plot=args.show_plot,
            save_plot=args.save_plot,
        )
    else:
        generate_all_plots(
            show_plot=args.show_plot,
            save_plot=args.save_plot,
        )


if __name__ == "__main__":
    main()