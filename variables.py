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

biomarker_data = {
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

optimal_biomarker_data = {
    "ethnicity": "western_europe",
    "metric": "us",
    "weight": "194",
    "height": "72",
    "smoke": "no",
    "csrfmiddlewaretoken": "4SdAofEdCaohTw7FZ2uHprZ7z4GAHhRZ",
    "Albumin": "5.1",
    "Glucose": "72.48",
    "Urea": "16.98",
    "Cholesterol": "100.0",
    "Protein_total": "6.15",
    "Sodium": "137.0",
    "Creatinine": "0.57",
    "Hemoglobin": "13.98",
    "Bilirubin_total": "0.05",
    "Triglycerides": "5.0",
    "HDL_Cholesterol": "40.83",
    "LDL_cholesterol": "47.3",
    "Calcium": "10.19",
    "Potassium": "4.42",
    "Hematocrit": "44.02",
    "MCHC": "35.66",
    "MCV": "79.0",
    "Platelets": "319.46",
    "Erythrocytes": "5.26"
}

biomarker_ranges = [
    {
        # 3.5 - 5.5 U/L
        "biomarker": "Albumin",
        "low_end": 3.5,
        "high_end": 5.5
    },
    {
        # 65 - 99 mg/dL
        "biomarker": "Glucose",
        "low_end": 65.0,
        "high_end": 99.0
    },
    {
        # 6 - 24 mg/dL
        "biomarker": "Urea",
        "low_end": 6.0,
        "high_end": 24.0
    },
    {
        # 100 - 199 mg/dL
        "biomarker": "Cholesterol",
        "low_end": 100.0,
        "high_end": 199.0
    },
    {
        # 6.0 - 8.5 g/dL
        "biomarker": "Protein_total",
        "low_end": 6.0,
        "high_end": 8.5
    },
    {
        # 134 - 144 mmol/L
        "biomarker": "Sodium",
        "low_end": 134.0,
        "high_end": 144.0
    },
    {
        # 0.57 - 1.00 mg/dL
        "biomarker": "Creatinine",
        "low_end": 0.57,
        "high_end": 1.00
    },
    {
        # 11.1 - 15.9 g/dL
        "biomarker": "Hemoglobin",
        "low_end": 11.1,
        "high_end": 15.9
    },
    {
        # 0.0 - 1.2 mg/dL
        "biomarker": "Bilirubin_total",
        "low_end": 0.05,
        "high_end": 1.2
    },
    {
        # 0 - 149 mg/dL
        "biomarker": "Triglycerides",
        "low_end": 5.0,
        "high_end": 149.0
    },
    {
        # > 39 mg/dL
        "biomarker": "HDL_Cholesterol",
        "low_end": 39.0,
        "high_end": 100.0
    },
    {
        # 0 - 99 mg/dL
        "biomarker": "LDL_cholesterol",
        "low_end": 5.0,
        "high_end": 99.0
    },
    {
        # 8.7 - 10.2 mg/dL
        "biomarker": "Calcium",
        "low_end": 8.7,
        "high_end": 10.2
    },
    {
        # 3.5 - 5.2 mmol/L
        "biomarker": "Potassium",
        "low_end": 3.5,
        "high_end": 5.2
    },
    {
        # 37 - 50 %
        "biomarker": "Hematocrit",
        "low_end": 37.0,
        "high_end": 50.0
    },
    {
        # 31.5 - 35.7 g/dL
        "biomarker": "MCHC",
        "low_end": 31.5,
        "high_end": 35.7
    },
    {
        # 79 - 97 fL
        "biomarker": "MCV",
        "low_end": 79.0,
        "high_end": 97.0
    },
    {
        # 150-379 103 /uL
        "biomarker": "Platelets",
        "low_end": 150,
        "high_end": 379
    },
    {
        # 3.77 - 5.28 106 /uL
        "biomarker": "Erythrocytes",
        "low_end": 3.77,
        "high_end": 5.28
    },
]