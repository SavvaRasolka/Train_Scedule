from kivy.uix.label import Label
from kivy.factory import Factory
from datetime import timedelta
from kivymd.uix.picker import MDTimePicker, MDDatePicker
from kivymd.uix.menu import MDDropdownMenu


class View:
    def __init__(self, screen, model):
        self.screen = screen
        self.model = model
        self.buffer = None
        self.note_per_page = 5
        self.current_page = 1
        self.num_of_pages = 1
        self.num_of_notes = 0
        self.note_per_current_page = 0

    def set_note_per_page(self, note_num):
        self.note_per_page = note_num
        self.current_page = 1
        self.show_table()

    def to_page(self, num_of_page):
        self.current_page = num_of_page
        self.show_table()

    def next_page(self):
        if self.current_page != self.num_of_pages:
            self.current_page = self.current_page + 1
        self.show_table()

    def previous_page(self):
        if self.current_page != 1:
            self.current_page = self.current_page - 1
        self.show_table()

    def show_table(self):
        self.update_attributes()
        self.screen.ids.note_on_page.text = "Записей на странице: " + str(self.note_per_current_page)
        self.screen.ids.all_notes.text = "Всего записей: " + str(self.num_of_notes)
        self.screen.ids.all_pages.text = "Всего страниц: " + str(self.num_of_pages)
        self.screen.ids.cur_page.text = str(self.current_page)
        start = (self.current_page - 1) * self.note_per_page
        hgt = (550 - self.note_per_page * 2) / self.note_per_page
        table = self.screen.ids.table
        table.clear_widgets(children=None)
        for x in range(start, start + self.note_per_current_page):
            table.add_widget(Label(size_hint=(1, None), height=hgt, color=(0, 0, 0, 1), text=self.model.data[x][0]))
            table.add_widget(Label(size_hint=(1, None), height=hgt, color=(0, 0, 0, 1), text=self.model.data[x][1]))
            table.add_widget(Label(size_hint=(1, None), height=hgt, color=(0, 0, 0, 1), text=self.model.data[x][2]))
            table.add_widget(Label(size_hint=(1, None), height=hgt, color=(0, 0, 0, 1),
                                   text=self.model.data[x][3].strftime('%Y.%d.%m %H:%M')))
            table.add_widget(Label(size_hint=(1, None), height=hgt, color=(0, 0, 0, 1),
                                   text=self.model.data[x][4].strftime('%Y.%d.%m %H:%M')))
            table.add_widget(Label(size_hint=(1, None), height=hgt, color=(0, 0, 0, 1),
                                   text=str(int(self.model.data[x][5] / timedelta(hours=1))) + "ч " + str(
                                       int((self.model.data[x][5] - timedelta(
                                           hours=int(self.model.data[x][5] / timedelta(hours=1)))) / timedelta(
                                           minutes=1))) + "мин"))

    def open_menu(self, button):
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": 'Добавить запись',
                "height": 56,
                "on_release": lambda: self.menu_action(1),
            },
            {
                "viewclass": "OneLineListItem",
                "text": 'Поиск',
                "height": 56,
                "on_release": lambda: self.menu_action(2),
            },
            {
                "viewclass": "OneLineListItem",
                "text": 'Удаление',
                "height": 56,
                "on_release": lambda: self.menu_action(3),
            },
            {
                "viewclass": "OneLineListItem",
                "text": 'Сохранение',
                "height": 56,
                "on_release": lambda: self.menu_action(4),
            },
            {
                "viewclass": "OneLineListItem",
                "text": 'Загрузка',
                "height": 56,
                "on_release": lambda: self.menu_action(5),
            }

        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )
        self.menu.caller = button
        self.menu.open()

    def menu_action(self, number):
        self.menu.dismiss()
        if number == 1:
            Factory.AddPopup().open()
        elif number == 2:
            Factory.SearchMenu().open()
        elif number == 3:
            Factory.DeletePopup().open()
        elif number == 4:
            Factory.SaveToFile().open()
        elif number == 5:
            Factory.LoadFromFile().open()

    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.set_time)
        time_dialog.open()

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.set_date)
        date_dialog.open()

    def set_time(self, instance, time):
        self.buffer.text = time.strftime('%H:%M')

    def set_date(self, instance, value, date):
        self.buffer.text = value.strftime('%Y.%d.%m')

    def update_attributes(self):
        add_page = 0
        if len(self.model.data) % self.note_per_page != 0:
            add_page = 1
        self.num_of_pages = len(self.model.data) // self.note_per_page + add_page
        self.num_of_notes = len(self.model.data)
        if self.num_of_notes // self.note_per_page < self.current_page:
            self.note_per_current_page = self.num_of_notes % self.note_per_page
        else:
            self.note_per_current_page = self.note_per_page

    def display_table(self, notes, table, label):
        table.clear_widgets(children=None)
        for x in notes:
            table.add_widget(Label(size_hint=(1, None), text=x[0]))
            table.add_widget(Label(size_hint=(1, None), text=x[1]))
            table.add_widget(Label(size_hint=(1, None), text=x[2]))
            table.add_widget(Label(size_hint=(1, None), text=x[3].strftime('%Y.%d.%m %H:%M')))
            table.add_widget(Label(size_hint=(1, None), text=x[4].strftime('%Y.%d.%m %H:%M')))
            table.add_widget(Label(size_hint=(1, None), text=str(int(x[5] / timedelta(hours=1))) + "ч " + str(
                int((x[5] - timedelta(hours=int(x[5] / timedelta(hours=1)))) / timedelta(minutes=1))) + "мин"))
        label.text = "Найденные записи: " + str(len(notes))
