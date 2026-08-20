import flet as ft

def main(page: ft.Page):
    page.title = "Джарвис"
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

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