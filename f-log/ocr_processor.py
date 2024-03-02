import requests
import uuid
import time
import json

def perform_ocr(api_url, secret_key, image_file):
    request_json = {
        'images': [
            {
                'format': 'jpeg',
                'name': 'demo'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [('file', open(image_file, 'rb'))]
    headers = {'X-OCR-SECRET': secret_key}

    response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
    result = response.json()

    # 결과 파일 저장 (옵션)
    with open('result.json', 'w', encoding='utf-8') as make_file:
        json.dump(result, make_file, indent="\t", ensure_ascii=False)

    text = ""
    for field in result['images'][0]['fields']:
        text += field['inferText']

    # 결과 텍스트 파일 저장 (옵션)
    with open('result.txt', 'w', encoding='utf-8') as file:
        file.write(text)

    return text
