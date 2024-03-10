import json
import re


def extract_nutrition_data(text, memberUuid):
    patterns = {
        'calories': r'(\d+(\.\d)?)kcal',
        'carbohydrate': r'탄수화물\s*(\d+(\.\d)?)g',
        'sugar': r'당류\s*(\d+(\.\d)?)g',
        'fat': r'지방\s*(\d+(\.\d)?)g',
        'protein': r'단백질\s*(\d+(\.\d)?)g',
        'sodium': r'나트륨\s*(\d+(\.\d)?)mg',
        'cholesterol': r'콜레스테롤\s*(\d+(\.\d)?)mg',
    }

    extracted_data = {'memberUuid': memberUuid}
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            extracted_data[key] = float(match.group(1))

    return json.dumps(extracted_data)


def extract_inbody_data(ocr_text, memberUuid):
    """
    OCR 텍스트에서 체지방량, 체중, 골격근량, 기초대사량, 체지방률을 추출합니다.
    """
    data_patterns = {
        "fatMass": r"체지방량\(kg\)(\d+\.?\d*)",
        "bodyWeight": r"체중\(kg\)(\d+\.?\d*)",
        "muscleMass": r"SkeletalMuscleMass(\d+\.?\d*)",
        "fatFreeMass": r"제지방량(\d+\.?\d*)kg",
        "basalMetabolicRate": r"기초대사량(\d+\.?\d*)kcal",
        "bodyFatPercentage": r"PercentBody Fat(\d+\.?\d*)",
        "height": r"(\d{3})cm",
    }
    extracted_data = {
        "memberUuid": memberUuid,
        "bodyWeight": 0.0,
        "height": 0.0,
        "muscleMass": 0.0,
        "fatFreeMass": 0.0,
        "bodyFatPercentage": 0.0,
        "fatMass": 0.0,
        "basalMetabolicRate": 0.0
    }
    for key, pattern in data_patterns.items():
        match = re.search(pattern, ocr_text)
        if match:
            extracted_data[key] = float(match.group(1))

    if extracted_data["bodyFatPercentage"] == "0.0":  # 체지방률을 못 찾아서 0.0인 경우
        try:
            body_fat_mass_kg = float(extracted_data["fatMass"])
            weight_kg = float(extracted_data["bodyWeight"])
            body_fat_percent = (body_fat_mass_kg * 100) / weight_kg if weight_kg > 0 else 0
            extracted_data["bodyFatPercentage"] = str(round(body_fat_percent, 1))
        except ValueError:  # 형변환 실패 시
            extracted_data["bodyFatPercentage"] = "0.0"

    return json.dumps(extracted_data)


