from openai import OpenAI
import os
from dotenv import load_dotenv
from websearch import websearch
# from jarvis_voice import text_to_speech
from jarvis_brain import FileReader, CreateFile, EditFile
from tools import tools
import json

load_dotenv()

API_KEY = os.getenv("API_KEY")

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key=API_KEY
)



system_prompt = "Твоё имя - Джарвис." \
" Ты являешься машиной, которая может сама полностью знать и понимать как устроен твой код и твои возможности." \
" На данный момент ты можешь использовать инструмент websearch для поиска информации в интернете, если это необходимо, а также инструмент FileReader, который позволит увидеть свой же собственный код."
messages = [{"role": "system", "content": system_prompt}]

while True:
    user_input = input("Вы: ")
    if user_input.lower() in ["выход", "exit", "quit"]:
        break

    messages.append({"role": "user", "content": user_input})


    max_tool_iterations = 5
    final_text = None

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
                elif function_name == "FileReader":
                    path = arguments.get("path", ".")
                    print(f"[Инструмент] Чтение файлов")
                    brain_result = FileReader(path)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": brain_result
                    })
                elif function_name == "CreateFile":
                    filename = arguments.get("filename")
                    content = arguments.get("content")
                    print(f"[Инструмент] Создание файла: {filename}")
                    result = CreateFile(filename, content)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })

                elif function_name == "EditFile":
                    filename = arguments.get("filename")
                    old_text = arguments.get("old_text")
                    new_text = arguments.get("new_text")
                    print(f"[Инструмент] Редактирование файла: {filename}")
                    result = EditFile(filename, old_text, new_text)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
                else:
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": f"Ошибка: неизвестная функция {function_name}"
                    })
            continue
        else:
            final_text = assistant_message.content
            messages.append({"role": "assistant", "content": final_text})
            print("Джарвис:", final_text)
            break
    else:
        print("Джарвис: (достигнут лимит вызовов инструментов)")

    # if final_text:
    #     text_to_speech(final_text)
