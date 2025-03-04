import flet as ft

from pageTimerList import PageTimerList

class Dashboard(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(page)        
        page.window.height = 640
        page.window.width = 360
        page.window.resizable = False
        page.window.maximizable = False
        page.window.minimizable = False

        self.page = page
        self.bg_color = "#192028"
        self.yellow_color = "#ffc107"
        self.dark_yellow_color = "#ff9800"
        self.green_color = "#1ab189"
        self.page.bgcolor = self.bg_color

        self.title = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.IconButton(icon=ft.icons.KEYBOARD_ARROW_DOWN, icon_color="white", on_click=self.page_timerlist),
                ft.Text(value="Timer", color="white", weight="bold"),
                ft.IconButton(icon=ft.icons.MORE_VERT_SHARP, icon_color="white"),
            ]
        )

        self.image = ft.Stack(
            height=200, width=200,
            alignment=ft.alignment.center,
            controls=[
                ft.Container(
                    height=180, width=180,
                    border_radius=90, bgcolor=self.yellow_color,
                ),

                ft.Container(
                    height=176, width=176,
                    border_radius=88, bgcolor=self.dark_yellow_color,
                ),

                ft.Container(
                    border_radius=70, width=140, height=140,
                    content=ft.Image(src="https://cdn-icons-png.flaticon.com/512/147/147144.png", fit=ft.ImageFit.COVER),
                    shadow=ft.BoxShadow(
                        blur_radius=20,
                        spread_radius=2,
                        color=ft.colors.with_opacity(0.5, self.yellow_color),
                        offset=ft.Offset(0, 0)
                    )
                )
            ]
        )

        self.time = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.Text("00:00", color=self.green_color, size=12),
                ft.Text("00:00", color=self.green_color, size=12),
            ]
        )

        self.music_name = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                ft.Text("First timer", color="white", size=12),
                ft.Text("Second tiemer", color=self.green_color, size=12),
            ]
        )

        self.options = ft.Container(
            height=40, width=130, border_radius=20,
            bgcolor=self.dark_yellow_color,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.IconButton(icon=ft.icons.ADD, bgcolor="transperent", icon_color=self.green_color),
                    ft.IconButton(icon=ft.icons.FAVORITE, bgcolor="transperent", icon_color=self.green_color),
                    ft.IconButton(icon=ft.icons.REMOVE, bgcolor="transperent", icon_color=self.green_color),
                ]
            )
        )

        self.controls_music = ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.LOOP, bgcolor="transperent", icon_color=self.green_color),
                ft.IconButton(icon=ft.icons.SKIP_PREVIOUS, bgcolor="transperent", icon_color=self.green_color),
                ft.IconButton(icon=ft.icons.PAUSE, bgcolor=self.yellow_color, icon_color="white", style=ft.ButtonStyle(
                    shadow_color=self.yellow_color,
                    elevation=5, padding=5
                )),
               ft.IconButton(icon=ft.icons.SKIP_NEXT, bgcolor="transperent", icon_color=self.green_color), 
               ft.IconButton(icon=ft.icons.SHUFFLE, bgcolor="transperent", icon_color=self.green_color),
            ]
        )

        self.progress_bar = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.IconButton(icon=ft.icons.VOLUME_MUTE, bgcolor="transperent", icon_color=self.green_color),
                ft.ProgressBar(value=0.8, bgcolor=self.dark_yellow_color, color=self.yellow_color,width=150, height=4),
                ft.IconButton(icon=ft.icons.VOLUME_UP_OUTLINED, bgcolor="transperent", icon_color=self.green_color),
            ]
        )

        self.page.add(
            ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.title,
                    self.image,
                    self.time,
                    self.music_name,
                    self.options,
                    self.controls_music,
                    self.progress_bar
                ]
            )
        )

    def page_timerlist(self, e):
        page = PageTimerList(self.page)
        self.page.views.append(page)
        self.page.update()

ft.app(target=Dashboard)
