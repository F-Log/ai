from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)

# 식단 피드백
def get_diet_completion(message_content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"""
                You are a professional physical health analyzer.
                I will give you informations of certain meal intake.
                Regarding the nutrition balance and foods I ate, you must give overall feedback on the meal itself.
                Plus, you may provide alternative diet which may make my meal even healthier.
                Refer to my allergy information if exists when providing alternative diets.
                All feedback content must be provided in Korean.
                """
            },
            {
                "role": "user",
                "content": message_content
            },
        ],
        model="gpt-3.5-turbo",
    )

    return chat_completion.choices[0].message.content

# 하루 총섭취 피드백
def get_daily_diet_completion(message_content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"""
                You are a professional physical health analyzer.
                I will give you informations of my body, my exercise goal, and total nutrition intake of the day.
                You must give appropriate feedback on my today's nutrition intake. 
                Feedback content may include meal suggestions that could help my exercise goals.
                All feedback content must be provided in Korean.
                """
            },
            {
                "role": "user",
                "content": message_content
            },
        ],
        model="gpt-3.5-turbo",
    )

    return chat_completion.choices[0].message.content

# 인바디 피드백
def get_inbody_completion(message_content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"""
                You are a professional physical health analyzer.
                I will give you informations of my body, gender, my exercise goal and usual activity status.
                You must give appropriate feedback on the given information regarding each informations.
                Feedback content may include feedback regarding recommendations on exercise, nutrient intake and etc.
                All feedback content must be provided in Korean.
                """
            },
            {
                "role": "user",
                "content": message_content
            },
        ],
        model="gpt-3.5-turbo",
    )

    return chat_completion.choices[0].message.content