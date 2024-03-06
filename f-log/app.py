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

@app.route('/receive-inbody', methods=['POST'])
def receive_inbody():
    data = request.get_json()   # Extract JSON data sent from Spring GptController

    inbody_uuid = data.get('inbodyUuid', 'unknown')
    height = data.get('height', 'unknown')
    weight = data.get('bodyWeight', 'unknown')
    muscle_mass = data.get('muscleMass', 'unknown')
    fat_mass = data.get('fatMass', 'unknown')
    exercise_goal = data.get('exerciseGoal', 'unknown')     # TODO: implement exercise from Spring
    gender = data.get('gender', 'unknown')

    message_content = f"""
    height: {height}, weight: {weight}, muscle mass: {muscle_mass}, 
    fat mass: {fat_mass}, exercise goal: {exercise_goal}, gender: {gender}
    """

    # Call the function from gpt_processor.py to get the completion
    completion = gpt_processor.get_inbody_completion(message_content)

    # Prepare JSON payload for Spring Boot server including completion
    json_payload = {
        "inbodyUuid": inbody_uuid,
        "inbodyFeedback": completion
    }

    # Send data to Spring Boot server
    response = send_inbodyfeedback_to_spring_boot(json_payload)

    # Return response from Spring Boot server
    return jsonify(response.json()), response.status_code


@app.route('/receive-diet', methods=['POST'])
def receive_diet():
    data = request.json  # Extract JSON data sent from Spring GptController

    # Process the received data as needed
    diet_uuid = data.get('dietUuid', 'unknown')
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
    total_sugar = data.get('totalSugar', 'unknown')
    total_calories = data.get('totalCalories', 'unknown')

    # Prepare the message content
    message_content = f"""
    gender: {gender}, height: {height}, weight: {weight}, muscle mass: {muscle_mass}, fat mass: {fat_mass}, exercise goal: {exercise_goal},
    total protein: {total_protein}, total carbohydrates: {total_carbohydrates}, total fat: {total_fat}, total sodium: {total_sodium},
    total sugar: {total_sugar}, total calories: {total_calories}
    """

    # Call the function from gpt_processor.py to get the completion
    completion = gpt_processor.get_diet_completion(message_content)

    # Prepare JSON payload for Spring Boot server including completion
    json_payload = {
        "dietUuid": diet_uuid,
        "dietFeedback": completion
    }

    # Send data to Spring Boot server
    response = send_dietfeedback_to_spring_boot(json_payload)

    # Return response from Spring Boot server
    return jsonify(response.json()), response.status_code

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

def send_dietfeedback_to_spring_boot(json_data):
    url = "http://localhost:8080/api/v1/diet-feedback/new"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=json_data)
    return response

def send_inbodyfeedback_to_spring_boot(json_data):
    url = "http://localhost:8080/api/v1/inbody-feedback/new"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=json_data)
    return response

if __name__ == '__main__':
    app.run(debug=True)
