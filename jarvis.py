from jarvis_core import JarvisAgent
from ui import main
import flet as ft


def print_tool_call(function_name, arguments):
    print(f"[Инструмент] {function_name}: {arguments}")


if __name__ == "__main__":
    ft.run(main)