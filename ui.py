import threading
import flet as ft
from jarvis_core import JarvisAgent


def main(page: ft.Page):
    page.title = "Джарвис"
    page.theme_mode = "dark"
    try:
        # Новый API (Flet >= 0.70)
        page.window.width = 480
        page.window.height = 760
    except AttributeError:
        # Старый API (Flet < 0.70)
        page.window_width = 480
        page.window_height = 760
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.START

    agent = JarvisAgent()

    chat_list = ft.ListView(expand=True, spacing=10, padding=20, auto_scroll=True)
    status_text = ft.Text("", size=12, italic=True, color=ft.Colors.AMBER_400)

    def add_bubble(text, is_user):
        bubble = ft.Container(
            content=ft.Text(text, selectable=True, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.BLUE_700 if is_user else ft.Colors.GREY_800,
            border_radius=14,
            padding=12,
        )
        row = ft.Row(
            [bubble],
            alignment=ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START,
        )
        chat_list.controls.append(row)
        page.update()

    def add_tool_note(function_name, arguments):
        note = ft.Text(
            f"🔧 {function_name}({arguments})",
            size=11,
            italic=True,
            color=ft.Colors.GREY_500,
        )
        chat_list.controls.append(ft.Row([note], alignment=ft.MainAxisAlignment.START))
        page.update()

    def on_tool_call(function_name, arguments):
        status_text.value = f"Использую инструмент: {function_name}..."
        page.update()
        add_tool_note(function_name, arguments)

    def set_input_enabled(enabled):
        input_field.disabled = not enabled
        send_button.disabled = not enabled
        page.update()

    def send_message(e):
        user_text = input_field.value.strip()
        if not user_text:
            return

        input_field.value = ""
        set_input_enabled(False)
        add_bubble(user_text, is_user=True)

        status_text.value = "Джарвис думает..."
        page.update()

        def worker():
            try:
                answer = agent.chat(user_text, on_tool_call=on_tool_call)
            except Exception as ex:
                answer = f"Произошла ошибка: {ex}"

            status_text.value = ""
            add_bubble(answer, is_user=False)
            set_input_enabled(True)

        threading.Thread(target=worker, daemon=True).start()

    input_field = ft.TextField(
        hint_text="Напишите сообщение Джарвису...",
        expand=True,
        border_radius=20,
        on_submit=send_message,
        shift_enter=True,
    )
    send_button = ft.IconButton(icon=ft.Icons.SEND, tooltip="Отправить", on_click=send_message)

    page.add(
        ft.Container(
            content=ft.Row(
                [ft.Text("Джарвис", size=20, weight=ft.FontWeight.BOLD), ft.Icon(ft.Icons.MIC)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.Padding(left=0, right=0, top=16, bottom=4),
        ),
        ft.Container(content=status_text, padding=ft.Padding(left=20, right=0, top=0, bottom=0)),
        chat_list,
        ft.Container(
            content=ft.Row([input_field, send_button]),
            padding=ft.Padding(left=16, right=16, top=10, bottom=10),
        ),
    )


