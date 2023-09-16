import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import json
import copy
import os


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


headers = {
    "Accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language":
    "en-US,en;q=0.9",
    "Cache-Control":
    "max-age=0",
    "Connection":
    "keep-alive",
    "Content-Type":
    "application/x-www-form-urlencoded",
    "Cookie":
    "csrftoken=4SdAofEdCaohTw7FZ2uHprZ7z4GAHhRZ; sessionid=89yfwgsb4v16hziorghgvloznyv17nzq",
    "DNT":
    "1",
    "Origin":
    "http://aging.ai",
    "Referer":
    "http://aging.ai/aging-v3/?m=us",
    "Upgrade-Insecure-Requests":
    "1",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
}

data = {
    "ethnicity": "western_europe",
    "metric": "us",
    "weight": "194",
    "height": "72",
    "smoke": "no",
    "csrfmiddlewaretoken": "4SdAofEdCaohTw7FZ2uHprZ7z4GAHhRZ",
    "Albumin": "4.7",
    "Glucose": "96",
    "Urea": "21",
    "Cholesterol": "102",
    "Protein_total": "6.8",
    "Sodium": "140",
    "Creatinine": "1.05",
    "Hemoglobin": "14.1",
    "Bilirubin_total": "0.4",
    "Triglycerides": "43",
    "HDL_Cholesterol": "59",
    "LDL_cholesterol": "31",
    "Calcium": "9.4",
    "Potassium": "4.6",
    "Hematocrit": "42.8",
    "MCHC": "32.9",
    "MCV": "88.4",
    "Platelets": "211",
    "Erythrocytes": "4.84"
}


def find_optimal_values(directory="predictions"):
    # For each prediction file, print the value which results in the lowest predicted age
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
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
                      optimal_age_prediction["value"] +
                      " results in a predicted age of " +
                      optimal_age_prediction["predicted_age"])


def save_predictions(biomarker, age_predictions):
    with open("predictions/" + biomarker + ".json", "w") as file:
        json.dump(age_predictions, file)


def test_levels(biomarker, low_end, high_end, step, data):
    age_predictions = []
    data_copy = copy.copy(data)

    for i in np.arange(low_end, high_end + step, step):
        i = round(i, 2)
        data_copy[biomarker] = i

        print("Calculating " + biomarker + " of " + str(i))

        # Request predicted age
        response = send_post_request(data_copy, headers)

        html_content = response.text
        predicted_age = extract_predicted_age(html_content)
        print("Prediction age: " + str(predicted_age))
        age_predictions.append({
            "biomarker": biomarker,
            "value": i,
            "predicted_age": predicted_age
        })

        time.sleep(5)

    print("\n### Finished calculations for " + biomarker + " ###\n")
    save_predictions(biomarker, age_predictions)


def test_all_levels():
    # 3.5 - 5.5 U/L
    test_levels("Albumin", 3.5, 5.5, 0.1, data)

    # 65 - 99 mg/dL
    test_levels("Glucose", 65.0, 99.0, 2, data)

    # 6 - 24 mg/dL
    test_levels("Urea", 6.0, 24.0, 1, data)

    # 100 - 199 mg/dL
    test_levels("Cholesterol", 100.0, 199.0, 5, data)

    # 6.0 - 8.5 g/dL
    test_levels("Protein_total", 6.0, 8.5, 0.1, data)

    # 134 - 144 mmol/L
    test_levels("Sodium", 134.0, 144.0, 0.5, data)

    # 0.57 - 1.00 mg/dL
    test_levels("Creatinine", 0.57, 1.00, 0.02, data)

    # 11.1 - 15.9 g/dL
    test_levels("Hemoglobin", 11.1, 15.9, 0.2, data)

    # 0.0 - 1.2 mg/dL
    test_levels("Bilirubin_total", 0.0, 1.2, 0.05, data)

    # 0 - 149 mg/dL
    test_levels("Triglycerides", 0.0, 149.0, 5, data)

    # > 39 mg/dL
    test_levels("HDL_Cholesterol", 39.0, 100.0, 2.5, data)

    # 0 - 99 mg/dL
    test_levels("LDL_cholesterol", 0.0, 99.0, 5, data)

    # 8.7 - 10.2 mg/dL
    test_levels("Calcium", 8.7, 10.2, 0.08, data)

    # 3.5 - 5.2 mmol/L
    test_levels("Potassium", 3.5, 5.2, 0.1, data)

    # 37 - 50 %
    test_levels("Hematocrit", 37.0, 50.0, 1, data)

    # 31.5 - 35.7 g/dL
    test_levels("MCHC", 31.5, 35.7, 0.25, data)

    # 79 - 97 fL
    test_levels("MCV", 79.0, 97.0, 1, data)

    # 150-379 103 /uL
    test_levels("Platelets", 150, 379, 10, data)

    # 3.77 - 5.28 106 /uL
    test_levels("Erythrocytes", 3.77, 5.28, 0.1, data)


test_all_levels()