import flet as ft


class PageTimerList(ft.View):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.bg_color = "#192028"
        self.green_color = "#1ab189"
        self.yellow_color = "#ffc107"
        self.dark_yellow_color = "#ff9800"
        self.bgcolor = self.bg_color

        self.controls.append(
            ft.Column(
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=self.yellow_color, on_click=self.close_page),
                            ft.Text(value="Timer List", color="white", weight="bold"),
                            ft.IconButton(icon=ft.icons.SEARCH, icon_color=self.yellow_color),
                            ft.IconButton(icon=ft.icons.MORE_VERT_SHARP, icon_color=self.yellow_color),
                        ]
                    ),

                    ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        controls=[
                            self.timer_list("image","First Timer","01:00",ft.Icons.PLAY_ARROW,self.dark_yellow_color,self.yellow_color),
                            ft.Divider(height=1, color=self.yellow_color),
                            self.timer_list("image","Second Timer","02:00",ft.Icons.PLAY_ARROW,self.dark_yellow_color,self.yellow_color),
                            ft.Divider(height=1, color=self.yellow_color),
                            self.timer_list("image","Third Timer","03:00",ft.Icons.PLAY_ARROW,self.dark_yellow_color,self.yellow_color),
                            ft.Divider(height=1, color=self.yellow_color),
                            self.timer_list("image","Fourth Timer","04:00",ft.Icons.PLAY_ARROW,self.dark_yellow_color,self.yellow_color),
                            ft.Divider(height=1, color=self.yellow_color),
                            self.timer_list("image","Fifth Timer","05:00",ft.Icons.PLAY_ARROW,self.dark_yellow_color,self.yellow_color),
                        ]
                    )
                ]
            ),
        )

    def timer_list(self, image, title, time, icon, color1, color2):
        return ft.Container(
            height=60, padding=5,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Image(src="https://cdn-icons-png.flaticon.com/512/147/147144.png", width=36, height=36, border_radius=18),
                    ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                        controls=[
                            ft.Text(value=title, color="white", size=14),
                            ft.Text(value=time, color=self.green_color, size=11),
                        ]
                    ),
                    ft.IconButton(icon=icon, icon_color="white"),
                    ft.IconButton(icon=ft.Icons.DELETE, icon_color=color2),
                    ft.IconButton(icon=ft.Icons.EDIT, icon_color="white"),
                ]
            )
        )

    def close_page(self, e):
        self.page.views.pop()
        self.page.update()