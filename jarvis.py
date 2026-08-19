from openai import OpenAI
import os
from dotenv import load_dotenv
from ddgs import DDGS
import json

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

# Описание инструмента для модели
tools = [
    {
        "type": "function",
        "function": {
            "name": "websearch",
            "description": "Ищет информацию в интернете по заданному запросу. Используй, когда нужны актуальные данные или факты, которых нет в твоей памяти.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Поисковый запрос"},
                    "max_results": {"type": "integer", "description": "Количество результатов", "default": 3}
                },
                "required": ["query"]
            }
        }
    }
]

system_prompt = "Твоё имя - Джарвис. Ты можешь использовать инструмент websearch для поиска информации в интернете, если это необходимо."
messages = [{"role": "system", "content": system_prompt}]

while True:
    user_input = input("Вы: ")
    if user_input.lower() in ["выход", "exit", "quit"]:
        break

    messages.append({"role": "user", "content": user_input})


    max_tool_iterations = 3
    for _ in range(max_tool_iterations):
        response = client.chat.completions.create(
            model="local-model",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.7
        )
        assistant_message = response.choices[0].message

        if assistant_message.tool_calls:
            messages.append(assistant_message.model_dump())

            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                if function_name == "websearch":
                    query = arguments.get("query")
                    max_results = arguments.get("max_results", 3)
                    print(f"[Инструмент] Поиск: {query}...")
                    search_result = websearch(query, max_results)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": search_result
                    })
                else:
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": f"Ошибка: неизвестная функция {function_name}"
                    })
            continue
        else:
            assistant_text = assistant_message.content
            messages.append({"role": "assistant", "content": assistant_text})
            print("Джарвис:", assistant_text)
            break
    else:
        print("Джарвис: (достигнут лимит вызовов инструментов)")