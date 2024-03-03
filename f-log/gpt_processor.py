from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)
def get_completion(message_content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"""
                You are a professional physical health analyzer.
                I will give you informations of my body, my exercise goal, and today's total food nutrition informations.
                You must give appropriate feedback on my today's diet.
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