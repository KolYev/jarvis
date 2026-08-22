from openai import OpenAI
import os
from dotenv import load_dotenv
import json

from websearch import websearch
from jarvis_brain import (
    FileReader,
    CreateFile,
    EditFile,
    CreateFolder,
    DeleteFile,
    DeleteFolder
)
from jarvis_memory import get_profile_text, update_profile, remember_fact, recall_facts
from tools import tools

load_dotenv()
API_KEY = os.getenv("API_KEY")


class JarvisAgent:
    """
    Инкапсулирует всю логику общения с моделью и вызова инструментов.
    Не зависит от того, как реализован интерфейс (консоль, Flet, что угодно).
    """

    def __init__(self):
        self.client = OpenAI(
            base_url="http://localhost:1234/v1",
            api_key=API_KEY
        )
        self.messages = [{"role": "system", "content": self._build_system_prompt()}]

    def _build_system_prompt(self):
        return (
            "Твоё имя - Джарвис."
            f"\n\nВот что ты знаешь о пользователе:\n{get_profile_text()}"
            " Ты являешься машиной, которая может сама полностью знать и понимать, как устроен твой код и твои возможности."
            " У тебя есть полный доступ к своей памяти через инструменты UpdateProfile, RememberFact, RecallFacts."
            " Используй их, чтобы знать максимум о пользователе, с которым общаешься."
            " Также ты можешь использовать инструмент websearch для поиска информации в интернете,"
            " инструмент FileReader для чтения файлов, CreateFile и EditFile для создания и редактирования файлов,"
            " CreateFolder для создания папок, DeleteFile и DeleteFolder для удаления."
            " Будь осторожен с удалением – оно необратимо."
        )

    def _dispatch_tool(self, function_name, arguments):
        if function_name == "websearch":
            return websearch(arguments.get("query"), arguments.get("max_results", 3))
        elif function_name == "UpdateProfile":
            return update_profile(arguments.get("key"), arguments.get("value"))
        elif function_name == "RememberFact":
            return remember_fact(arguments.get("fact"))
        elif function_name == "RecallFacts":
            return recall_facts(arguments.get("query"))
        elif function_name == "FileReader":
            return FileReader(arguments.get("path", "."))
        elif function_name == "CreateFile":
            return CreateFile(arguments.get("filename"), arguments.get("content"))
        elif function_name == "EditFile":
            return EditFile(arguments.get("filename"), arguments.get("old_text"), arguments.get("new_text"))
        elif function_name == "CreateFolder":
            return CreateFolder(arguments.get("path"))
        elif function_name == "DeleteFile":
            return DeleteFile(arguments.get("path"))
        elif function_name == "DeleteFolder":
            return DeleteFolder(arguments.get("path"))
        else:
            return f"Ошибка: неизвестная функция {function_name}"

    def chat(self, user_input, on_tool_call=None, max_tool_iterations=20):
        """
        Отправляет сообщение пользователя модели, прогоняет цикл вызова инструментов
        и возвращает финальный текстовый ответ.

        on_tool_call: необязательный callback(function_name, arguments),
        вызывается перед каждым использованием инструмента — удобно для
        отображения в UI ("Джарвис ищет в интернете...", "Джарвис читает файл...").
        """
        self.messages.append({"role": "user", "content": user_input})

        for _ in range(max_tool_iterations):
            response = self.client.chat.completions.create(
                model="local-model",
                messages=self.messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.7
            )
            assistant_message = response.choices[0].message

            if assistant_message.tool_calls:
                self.messages.append(assistant_message.model_dump())

                for tool_call in assistant_message.tool_calls:
                    function_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)

                    if on_tool_call:
                        on_tool_call(function_name, arguments)

                    result = self._dispatch_tool(function_name, arguments)
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
                continue
            else:
                final_text = assistant_message.content
                self.messages.append({"role": "assistant", "content": final_text})
                return final_text

        return "(достигнут лимит вызовов инструментов)"