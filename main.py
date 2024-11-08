import flet as ft
import json


class App(ft.Container):
    def __init__(self, page):
        super().__init__()

        # open settings 

        self.settings_json = json.load(open('./settings.json', 'r'))

        self.page = page

        self.add_button = ft.IconButton(icon=ft.icons.ADD_TASK, 
                                    icon_color="white",
                                    on_click=self.add_task,
                                    bgcolor='#606c38',
                                )

        self.new_task_input = ft.TextField(label="Nueva tarea", 
                            hint_text="Nueva tarea", 
                            border_color='white',
                            cursor_color='white',
                            border_radius=10,

                           )
        
        self.title = ft.Container(
            margin=ft.margin.only(bottom=10, top=20),
            content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    
                    controls=[
                        ft.Row(
                            controls=[

                                ft.Image(
                                    src="./assets/scriptura_white.png",
                                    width=20,
                                ),
                                ft.Text('Scriptura', size=20),

                            ]
                        ),

                        ft.IconButton(ft.icons.SETTINGS, icon_color='white', on_click=self.change_page, data="1"),
                    ]
            )
        )

        self.main_control = ft.Container(
            height=70,
            content=ft.ResponsiveRow(
                    controls=[
                        ft.Column(col={'xs': 10, 'md': 9, 'lg': 10}, controls=[self.new_task_input]),
                        ft.Column(col={'xs': 2, 'md': 3, 'lg': 2}, controls=[self.add_button])
                    ]
            )
        )

        if self.settings_json["wallpaper"] == "":
            self.settings_json["wallpaper"] = './assets/background.jpeg'


        self.tasks_container = ft.Container(
            border_radius=20,
            expand=True,
            content=ft.Stack(
                expand=True,
                controls=[
                    ft.Image(
                        src=self.settings_json["wallpaper"],
                        fit=ft.ImageFit.COVER,
                        width=self.page.width,
                        opacity=0.7,

                    ),

                    ft.Column(
                        scroll='hidden',
                        controls=[

                        ]
                    )

                ]
            )

        )

        # CONFIGURATION 

        self.configuration_main = ft.Container(
            width=self.page.width,
            height=80,
            padding=ft.padding.only(left=10, right=10),
            bgcolor='black',
            border_radius=10,
            content=ft.Row(
                controls=[
                    ft.IconButton(ft.icons.ARROW_BACK, 
                    icon_color='white', data='2', on_click=self.change_page),
                    ft.Text('Configuración', size=20),
                ]
                
            )
        )

        self.file_picker = ft.FilePicker(
            on_result=self.change_background,

        )

        page.overlay.append(self.file_picker)

        self.settings = ft.Column(
            expand=True,
            controls=[
                ft.TextButton(text="Cambiar fondo", 
                                width=self.page.width,
                                style=ft.ButtonStyle(
                                    color=ft.colors.WHITE,
                                    bgcolor='#606c38',  
                                    overlay_color=ft.colors.BLACK,
                                    shape=ft.RoundedRectangleBorder(radius=0)  
                                ),
                                on_click=lambda e: self.file_picker.pick_files()
                            )
            ]
        )
        self.page.bgcolor = "#283618"  
        self.page.add(

            ft.Column(

                expand=True,
                controls=[
                    ft.Stack(
                        
                        expand=True,
                        controls=[
                            ft.Container(
                                bgcolor='#283618',
                                offset=ft.transform.Offset(0, 0),
                                expand=True,
                                content=ft.Column(
                                    controls=[
                                        self.title,
                                        self.main_control,
                                        self.tasks_container
                                        ]
                                    )
                                ),

                            ft.Container(
                                bgcolor='#283618',
                                offset=ft.transform.Offset(2, 0),
                                width=self.page.width,
                                expand=True,
                                content=ft.Column(
                                    controls=[
                                            self.configuration_main,
                                            self.settings
                                        ]
                                    )
                                ),
                        ]
                    )                    
                ]
            ),                  
        )

        self.view_tasks()

    def find_index(self, tasks, task_id):
        for index, task in enumerate(tasks):
            if task['id'] == task_id:
                return index
        return None
            
    def delete_task(self, e):
        with open('./tasks.json', 'r+') as task_file:
            data = json.load(task_file)
            task_file.seek(0)
            index = self.find_index(data['tasks'], e.control.data)
            del data['tasks'][index]
            json.dump(data, task_file, indent=4)
            task_file.truncate()
        self.view_tasks()

    def checking(self, e):


        with open('./tasks.json', 'r+') as task_file:
            data = json.load(task_file)
            task_file.seek(0)
            index = self.find_index(data['tasks'], e.control.data)
            
            if data['tasks'][index]['completed'] == True:
                data['tasks'][index]['completed'] = False
            else:
                data['tasks'][index]['completed'] = True



            json.dump(data, task_file, indent=4)
            task_file.truncate()
        self.view_tasks()


    def view_tasks(self):
        with open('./tasks.json', 'r+') as task_file:
            data = json.load(task_file)

            self.tasks_container.content.controls[1].controls.clear()
            
            for task in data['tasks']:
                current_task = ft.Container(
                margin=ft.margin.only(left=5, right=5, top=10),
                padding=ft.padding.only(left=5),
                bgcolor='#606c38',
                border_radius=30,
                alignment=ft.alignment.center,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            width=self.page.width,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Checkbox(check_color='white', active_color='#606c38', value=task['completed'], on_change=self.checking, data=task['id']),
                                ft.Container(
                                    expand=True,
                                    margin=ft.margin.only(top=5, bottom=5),
                                    content=ft.Text(
                                        task['description'], 
                                        size=14,
                                        max_lines=3,
                                        overflow=ft.TextOverflow.CLIP,
                                        color='white',
                                        text_align=ft.TextAlign.CENTER,

                                        )
                                    ),
                                
                                    ft.IconButton(icon=ft.icons.DELETE, icon_color='white', on_click=self.delete_task, data=task['id'])
                                ]
                            )
                        ]
                    )
                )
                
                self.tasks_container.content.controls[1].controls.append(current_task)
        self.page.update()


    def add_task(self, e):
        task = self.new_task_input.value
        if task == '':
            return None
        
        with open('./tasks.json', 'r+') as task_file:
            data = json.load(task_file)
            task_file.seek(0)
            task_id = len(data['tasks'])
            task_id += 1
            data['tasks'].append(
                {'id': task_id, 'completed': False, 'description': task}
            )

            json.dump(data, task_file, indent=4)
            task_file.truncate()

        self.new_task_input.value = ''
        self.view_tasks()
        


    def change_page(self, e):
        if e.control.data == "1":
            self.page.controls[0].controls[0].controls[0].offset = ft.transform.Offset(2, 0)
            self.page.controls[0].controls[0].controls[1].offset = ft.transform.Offset(0, 0)
        if e.control.data == "2":
            self.page.controls[0].controls[0].controls[0].offset = ft.transform.Offset(0, 0)
            self.page.controls[0].controls[0].controls[1].offset = ft.transform.Offset(2, 0)
        self.page.update()

    def change_background(self, e):
        if e.files:
            file = e.files[0]
            img_path = file.path
            self.tasks_container.content.controls[0].src = img_path

            with open('./settings.json', 'r+') as f:
                data = json.load(f)
                f.seek(0)
                data['wallpaper'] = img_path
                json.dump(data, f, indent=4)
                f.truncate() 



            



ft.app(App,  assets_dir="assets")
    











    