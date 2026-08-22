from jarvis_core import JarvisAgent


def print_tool_call(function_name, arguments):
    print(f"[Инструмент] {function_name}: {arguments}")


if __name__ == "__main__":
    agent = JarvisAgent()
    print("Джарвис готов к работе (введите 'выход', 'exit' или 'quit' для завершения)")

    while True:
        user_input = input("Вы: ")
        if user_input.lower() in ["выход", "exit", "quit"]:
            break

        answer = agent.chat(user_input, on_tool_call=print_tool_call)
        print("Джарвис:", answer)