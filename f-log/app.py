from dotenv import load_dotenv
from flask import Flask, request, jsonify
import os
import ocr_processor
import data_extractor
import requests
import gpt_processor

app = Flask(__name__)
load_dotenv()
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/receive-diet', methods=['POST'])
def receive_diet():
    data = request.json  # Extract JSON data sent from Spring DietController

    # Process the received data as needed
    gender = data.get('gender', 'unknown')
    height = data.get('height', 'unknown')
    weight = data.get('bodyWeight', 'unknown')
    muscle_mass = data.get('muscleMass', 'unknown')
    fat_mass = data.get('fatMass', 'unknown')
    exercise_goal = data.get('exerciseGoal', 'unknown')
    total_protein = data.get('totalProtein', 'unknown')
    total_carbohydrates = data.get('totalCarbohydrate', 'unknown')
    total_fat = data.get('totalFat', 'unknown')
    total_sodium = data.get('totalSodium', 'unknown')

    # Prepare the message content
    message_content = f"""
    gender: {gender}, height: {height}, weight: {weight}, muscle mass: {muscle_mass}, fat mass: {fat_mass}, exercise goal: {exercise_goal},
    total protein: {total_protein}, total carbohydrates: {total_carbohydrates}, total fat: {total_fat}, total sodium: {total_sodium}
    """

    print(message_content)

    # Call the function from gpt_processor.py to get the completion
    completion = gpt_processor.get_completion(message_content)

    print(completion)
    return completion, 200

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
