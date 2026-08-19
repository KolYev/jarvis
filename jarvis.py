from openai import OpenAI
import os
from dotenv import load_dotenv
from duckduckgo_search import DDGS

load_dotenv()

API_KEY = os.getenv("API_KEY")

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key=API_KEY
)

# поиск информации в DuckDuckGo
def websearch(query, max_results=3):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
    if not results:
        return "Ничего не найдено."
    snippets = []
    for r in results:
        snippets.append(f"Заголовок: {r['title']}\nСсылка: {r['href']}\nТекст: {r['body']}")
    return "\n\n".join(snippets)

print("Вы: ", end="")
message = str(input())

prompt = ("Твоё имя - Джарвис. Используй информацию из своей памяти и из результатов поиска для ответов на вопросы.")

responce = client.chat.completions.create(
    model="local-model",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": message}
    ],
    temperature=0.7
)

print(responce.choices[0].message.content)