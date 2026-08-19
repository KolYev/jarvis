from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key=API_KEY
)

responce = client.chat.completions.create(
    model="local-model",
    messages=[
        {"role": "system", "content": "Твоё имя - Джарвис"},
        {"role": "user", "content": "Привет! Как тебя зовут?"}
    ],
    temperature=0.7
)

print(responce.choices[0].message.content)