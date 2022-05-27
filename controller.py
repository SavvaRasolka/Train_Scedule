from kivy.factory import Factory
from datetime import datetime, timedelta


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def check_if_time_in_past(self, delta):
        if delta != abs(delta):
            return True
        else:
            return False

    def check_for_train_number(self, train):
        try:
            int(train.text)
            return False
        except:
            return True

    def check_for_train_repeat(self, train_num, dep_d):
        if not bool(self.model.data):
            return False
        else:
            if isinstance(train_num, str):
                for each_train in self.model.data:
                    if train_num == each_train[0] and dep_d.date() == each_train[3].date():
                        return True
            else:
                for each_train in self.model.data:
                    if train_num.text == each_train[0] and dep_d.date() == each_train[3].date():
                        return True
            return False

    def add_note(self, popup, train, st_from, st_to, dep_d, dep_t, arr_d, arr_t):
        try:
            if self.check_for_train_number(train):
                Factory.MsgAddNumberPopup().open()
                return 0
            depature = datetime.strptime(dep_d.text + '-' + dep_t.text, '%Y.%d.%m-%H:%M')
            arrival = datetime.strptime(arr_d.text + '-' + arr_t.text, '%Y.%d.%m-%H:%M')
            travel_time = arrival - depature
            if self.check_if_time_in_past(travel_time):
                Factory.MsgAddPastPopup().open()
                return 0
            if self.check_for_train_repeat(train, depature):
                Factory.MsgAddRepeatPopup().open()
                popup.dismiss()
                return 0
            self.model.add_note(train.text, st_from.text, st_to.text, depature, arrival, travel_time)
            popup.dismiss()
            self.view.show_table()
        except:
            Factory.MsgAddEmptyPopup().open()

    def add_note_from_file(self, train, st_from, st_to, dep_d, arr_d):
        departure = datetime.strptime(dep_d, '%Y.%d.%m-%H:%M')
        arrival = datetime.strptime(arr_d, '%Y.%d.%m-%H:%M')
        travel_time = arrival - departure
        if not self.check_for_train_repeat(train, departure):
            return self.model.add_note(train, st_from, st_to, departure, arrival, travel_time)

    def search_by_number(self, num_of_train, table, label):
        result_of_search = self.model.search_by_number(num_of_train.text)
        self.view.display_table(result_of_search, table, label)

    def search_by_station(self, dep_or_arr, station, table, label):
        index = 1
        if dep_or_arr == 'arr':
            index = 2
        result_of_search = self.model.search_by_station(index, station.text)
        self.view.display_table(result_of_search, table, label)

    def search_by_time(self, dep_or_arr, min, max, table, label):
        try:
            min_time = datetime.strptime(min.text, '%H:%M')
            max_time = datetime.strptime(max.text, '%H:%M')
            min_time = datetime(1, 1, 1, min_time.hour, min_time.minute)
            max_time = datetime(1, 1, 1, max_time.hour, max_time.minute)
            index = 3
            if min_time > max_time:
                Factory.MsgSearchPastPopup().open()
            if dep_or_arr == 'arr':
                index = 4
            result_of_search = self.model.search_by_time(min_time, max_time, index)
            self.view.display_table(result_of_search, table, label)
        except:
            Factory.MsgPopup().open()

    def search_by_travel_time(self, hours_input, minutes_input, table, label):
        try:
            travel_time = timedelta(hours=int(hours_input.text), minutes=int(minutes_input.text))
            result_of_search = self.model.search_by_travel_time(travel_time)
            self.view.display_table(result_of_search, table, label)
        except:
            Factory.MsgPopup().open()

    def delete_by_number(self, num_of_train, table, label):
        result_of_search = self.model.search_by_number(num_of_train, table, label)
        self.view.display_table(result_of_search, table, label)
        self.model.delete_trains(result_of_search)

    def delete_by_station(self, dep_or_arr, station, table, label):
        result_of_search = self.model.search_by_station(dep_or_arr, station, table, label)
        self.view.display_table(result_of_search, table, label)
        self.model.delete_trains(result_of_search)

    def delete_by_time(self, dep_or_arr, min, max, table, label):
        result_of_search = self.model.search_by_time(dep_or_arr, min, max, table, label)
        self.view.display_table(result_of_search, table, label)
        self.model.delete_trains(result_of_search)

    def delete_by_travel_time(self, hours, minutes, table, label):
        result_of_search = self.model.search_by_travel_time(hours, minutes, table, label)
        self.view.display_table(result_of_search, table, label)
        self.model.delete_trains(result_of_search)
