from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)
def get_diet_completion(message_content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"""
                You are a professional physical health analyzer.
                I will give you informations of my body, my exercise goal, and total nutrition intake of the day.
                You must give appropriate feedback on my today's nutrition intake. 
                Feedback content may include meal suggestions that could help my exercise goals.
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

def get_inbody_completion(message_content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"""
                You are a professional physical health analyzer.
                I will give you informations of my body, gender, and my exercise goal.
                You must give appropriate feedback on the given information regarding the exercise goal and gender.
                Feedback content may include feedback regarding recommendations on exercise, nutrient intake and etc.
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