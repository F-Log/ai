from dotenv import load_dotenv
from flask import Flask, request, jsonify
import os
import ocr_processor
import data_extractor
import requests

app = Flask(__name__)
load_dotenv()
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    # memberUuid form-data에서 추출
    memberUuid = request.form.get('memberUuid', None)
    if not memberUuid:
        return jsonify({'error': 'No memberUuid provided'}), 400

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 파일 저장
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # OCR 처리
    api_url = os.getenv('API_URL')
    secret_key = os.getenv('SECRET_KEY')
    if not api_url or not secret_key:
        return jsonify({'error': 'API URL or Secret Key not configured'}), 500

    ocr_text = ocr_processor.perform_ocr(api_url, secret_key, file_path)

    # 데이터 추출 및 JSON 형식으로 변환, member_uuid 포함
    json_data = data_extractor.extract_nutrition_data(ocr_text, memberUuid)

    # Spring Boot 애플리케이션으로 데이터 전송
    response = send_data_to_spring_boot(json_data)

    # 임시 파일 삭제
    os.remove(file_path)

    return response.text

def send_data_to_spring_boot(json_data):
    url = "http://localhost:8080/api/v1/food/new"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json_data)
    return response

if __name__ == '__main__':
    app.run(debug=True)
