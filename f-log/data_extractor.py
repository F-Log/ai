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
