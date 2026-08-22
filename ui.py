import flet as ft

def main(page: ft.Page):
    page.title = "Джарвис"
    page.theme_mode = 'dark'
    page.window_width = 480
    page.window_height = 760
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.START

    page.add(
        ft.Row(
            [ 
                ft.Text('Джарвис'),
                ft.Icon(icon=ft.Icons.MIC)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.app(target=main)