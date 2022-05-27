from kivy import Config
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.factory import Factory
import xml.etree.ElementTree as ET
import xml.sax
from model import Model
from controller import Controller
from view import View

Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'height', 750)
Config.set('graphics', 'width', 1200)
Config.write()


class MainWindow(Widget):
    pass


class TableApp(MDApp):

    def build(self):
        screen = MainWindow()
        model = Model()
        view = View(screen, model)
        self.view = view
        self.controller = Controller(model, view)
        self.title = "Train Schedule"
        return screen

    def selected(self, filename):
        try:
            handler = TableHandler()
            handler.parser.setContentHandler(handler)
            handler.parser.parse(filename[0])
            if handler.error_index:
                Factory.MsgFileMissedPopup().open()
            for each_train in handler.trains:
                self.controller.add_note_from_file(each_train[0], each_train[1], each_train[2],
                                                   each_train[3], each_train[4])
            self.view.show_table()
        except:
            Factory.MsgFilePopup().open()

    def save_to_file(self, path):
        saving = TableSaver(self.controller.model.data)
        saving.save(path)


class TableHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.parser = xml.sax.make_parser()
        self.error_index = False
        self.CurrentData = ""
        self.trains = []
        self.one_train = []
        self.arrival = ''
        self.train_number = ''
        self.station_departure = ''
        self.station_arrival = ''
        self.departure = ''
        self.dict_of_fields = {'train_number': False, 'station_departure': False, 'station_arrival': False,
                               'departure': False, 'arrival': False}

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if self.CurrentData == "train":
            pass

    def characters(self, content):
        if self.CurrentData == "train_number":
            self.train_number = content
            self.dict_of_fields['train_number'] = True
        elif self.CurrentData == "station_departure":
            self.station_departure = content
            self.dict_of_fields['station_departure'] = True
        elif self.CurrentData == "station_arrival":
            self.station_arrival = content
            self.dict_of_fields['station_arrival'] = True
        elif self.CurrentData == "departure":
            self.departure = content
            self.dict_of_fields['departure'] = True
        elif self.CurrentData == "arrival":
            self.arrival = content
            self.dict_of_fields['arrival'] = True

    def endElement(self, tag):

        if self.CurrentData == "train_number":
            self.one_train.append(self.train_number)
        elif self.CurrentData == "station_departure":
            self.one_train.append(self.station_departure)
        elif self.CurrentData == "station_arrival":
            self.one_train.append(self.station_arrival)
        elif self.CurrentData == "departure":
            self.one_train.append(self.departure)
        elif self.CurrentData == "arrival":
            self.one_train.append(self.arrival)
        if len(self.one_train) == 5:
            index = True
            for key, value in self.dict_of_fields.items():
                if value is False:
                    self.error_index = True
                    print(key)
                    index = False
                self.dict_of_fields[key] = False

            if index:
                self.trains.append(self.one_train)
            self.arrival = ''
            self.train_number = ''
            self.station_departure = ''
            self.station_arrival = ''
            self.departure = ''
            self.one_train = []
            self.CurrentData = ''


class TableSaver:
    def __init__(self, data):
        self.data = data

    def save(self, path):
        root = ET.Element('data')
        for note in self.data:
            train = ET.Element('train')

            train_number = ET.Element('train_number')
            train_number.text = str(note[0])
            train.append(train_number)

            st_dep = ET.Element('station_departure')
            st_dep.text = note[1]
            train.append(st_dep)

            st_arr = ET.Element('station_arrival')
            st_arr.text = note[2]
            train.append(st_arr)

            departure = ET.Element('departure')
            departure.text = note[3].strftime('%Y.%d.%m-%H:%M')
            print(note[3])
            train.append(departure)

            arrival = ET.Element('arrival')
            arrival.text = note[4].strftime('%Y.%d.%m-%H:%M')
            train.append(arrival)

            root.append(train)
        etree = ET.ElementTree(root)
        print(path + "\\train_table.xml")
        try:
            file_to_save = open(path + "\\train_table.xml", "wb")
            etree.write(file_to_save, encoding='utf-8', xml_declaration=True)
        except:
            Factory.MsgFilePopup().open()


if __name__ == '__main__':
    TableApp().run()
