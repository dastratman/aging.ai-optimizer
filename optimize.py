import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import json
import copy
import os
import numpy as np
import matplotlib.pyplot as plt
from variables import headers, biomarker_data, optimal_biomarker_data, biomarker_ranges


def extract_predicted_age(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    result_div = soup.find('div', class_='aging41_results')
    h2_tag = result_div.find('h2')
    if h2_tag:
        text = h2_tag.get_text()
        # Extract the numeric value from the text
        age = float(text.split(":")[1].strip().split(" ")[0])
        return age
    return None


def send_post_request(data, headers):

    url = "http://aging.ai/aging-v3/?m=us"

    response = requests.post(
        url, headers=headers, data=data,
        verify=False)  # verify=False is equivalent to --insecure
    return response


def generate_plots():
    for filename in os.listdir("predictions"):
        if filename.endswith('.json'):
            biomarker = filename.replace('.json', '')
            calculate_regression(biomarker, show_plot=False, save_plot=True)


def find_optimal_real_values():
    # For each prediction file, print the value which results in the lowest predicted age
    for filename in os.listdir("predictions"):
        if filename.endswith('.json'):
            filepath = os.path.join("predictions", filename)
            with open(filepath, 'r') as json_file:
                age_predictions = json.load(json_file)
                biomarker = age_predictions[0]['biomarker']

                optimal_age_prediction = {
                    "biomarker": biomarker,
                    "value": 0,
                    "predicted_age": 100
                }

                for age_prediction in age_predictions:
                    if age_prediction['predicted_age'] < optimal_age_prediction[
                            'predicted_age']:
                        optimal_age_prediction = age_prediction

                print("The optimal value for " + biomarker + " of " +
                      str(optimal_age_prediction["value"]) +
                      " results in a predicted age of " +
                      str(optimal_age_prediction["predicted_age"]))


def calculate_2nd_degree(age_predictions, low_end, high_end):
    x_list = [item['value'] for item in age_predictions]
    y_list = [item['predicted_age'] for item in age_predictions]

    x = np.array(x_list)
    y = np.array(y_list)

    coef2 = np.polyfit(x, y, 2)

    x_calc = list(np.arange(low_end, high_end, (high_end - low_end) / 100))
    y_calc = np.polyval(coef2, x_calc)

    index_of_lowest_value = np.argmin(y_calc)
    print(round(x_calc[index_of_lowest_value], 2))


def find_optimal_calc_values():
    print(len(biomarker_ranges))
    for biomarker_range in biomarker_ranges:
        biomarker = biomarker_range['biomarker']
        low_end = biomarker_range['low_end']
        high_end = biomarker_range['high_end']

        print('Calculating optimal value for ' + biomarker)

        age_predictions = []
        with open("predictions/" + biomarker + ".json", 'r') as json_file:
            age_predictions = json.load(json_file)

        calculate_2nd_degree(age_predictions, low_end, high_end)


def save_predictions(biomarker, age_predictions):
    with open("predictions/" + biomarker + ".json", "w") as file:
        json.dump(age_predictions, file)


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


def calculate_regression(biomarker, show_plot=False, save_plot=True):
    print('\nPlotting ' + biomarker)

    age_predictions = []
    with open("predictions/" + biomarker + ".json", 'r') as json_file:
        age_predictions = json.load(json_file)

    x_list = [item['value'] for item in age_predictions]
    y_list = [item['predicted_age'] for item in age_predictions]

    x = np.array(x_list)
    y = np.array(y_list)

    coef1 = np.polyfit(x, y, 1)
    m, b = coef1  # slope and intercept
    y_pred1 = np.polyval(coef1, x)
    rr1 = calculate_coefficient_of_determination(x, y, 1)

    # Fit 2nd degree polynomial
    coef2 = np.polyfit(x, y, 2)
    y_pred2 = np.polyval(coef2, x)
    rr2 = calculate_coefficient_of_determination(x, y, 2)

    # Fit 3rd degree polynomial
    coef3 = np.polyfit(x, y, 3)
    y_pred3 = np.polyval(coef3, x)
    rr3 = calculate_coefficient_of_determination(x, y, 3)

    # Plot the data
    plt.scatter(x, y, color='blue', label='Data points')

    # Plot the polynomial regression lines
    plt.plot(x,
             y_pred1,
             color='red',
             label=f'1st Degree: y = {m:.2f}x + {b:.2f} | RR: {rr1:.2f}')
    plt.plot(
        x,
        y_pred2,
        color='green',
        label=
        f'2nd Degree: y = {coef2[0]:.2f}x^2 + {coef2[1]:.2f}x + {coef2[2]:.2f} | RR: {rr2:.2f}'
    )
    plt.plot(
        x,
        y_pred3,
        color='purple',
        label=
        f'3rd Degree: y = {coef3[0]:.2f}x^3 + {coef3[1]:.2f}x^2 + {coef3[2]:.2f}x + {coef3[3]:.2f} | RR: {rr3:.2f}'
    )

    print(f'1st Degree: y = {m:.2f}x + {b:.2f}')
    print(f'RR: {rr1:.2f}')
    print(
        f'2nd Degree: y = {coef2[0]:.2f}x^2 + {coef2[1]:.2f}x + {coef2[2]:.2f}'
    )
    print(f'RR: {rr2:.2f}')
    print(
        f'3rd Degree: y = {coef3[0]:.2f}x^3 + {coef3[1]:.2f}x^2 + {coef3[2]:.2f}x + {coef3[3]:.2f}'
    )
    print(f'RR: {rr3:.2f}')

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


def request_age(data):
    response = send_post_request(data, headers)

    html_content = response.text
    predicted_age = extract_predicted_age(html_content)
    return predicted_age


def iterate_levels(biomarker, low_end, high_end, step, data):
    age_predictions = []
    data_copy = copy.copy(data)

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

        time.sleep(5)

    print("\n### Finished calculations for " + biomarker + " ###\n")
    save_predictions(biomarker, age_predictions)


def test_all_levels(biomarker_ranges, biomarker_data):
    for biomarker_range in biomarker_ranges:
        biomarker = biomarker_range['biomarker']
        low_end = biomarker_range['low_end']
        high_end = biomarker_range['high_end']
        step = (high_end - low_end) / 20

        iterate_levels(biomarker, low_end, high_end, step, biomarker_data)


# test_all_levels(biomarker_ranges, biomarker_data)

# calculate_regression("Protein_total")

# find_optimal_values()

# generate_plots()

# find_optimal_calc_values()

predicted_age = request_age(optimal_biomarker_data)
print('Predicted age: ' + str(predicted_age))