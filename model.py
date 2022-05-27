from datetime import datetime


class Model:
    def __init__(self):
        self.data = []

    def add_note(self, train, st_from, st_to, depature, arrival, travel_time):
        self.data.append([train, st_from, st_to, depature, arrival, travel_time])

    def search_by_number(self, train_num):
        result = []
        for note in self.data:
            if note[0] == train_num:
                result.append(note)
        return result

    def search_by_station(self, index, station):
        result = []
        for note in self.data:
            if note[index] == station:
                result.append(note)
        return result

    def search_by_time(self, min, max, index):
        result_of_search = []
        for note in self.data:
            dep_time = datetime(1, 1, 1, note[index].hour, note[index].minute)
            if min <= dep_time <= max:
                result_of_search.append(note)
        return result_of_search

    def search_by_travel_time(self, travel):
        result_of_search = []
        for note in self.data:
            if note[5] == travel:
                result_of_search.append(note)
        return result_of_search

    def delete_trains(self, list_of_tr):
        for del_el in list_of_tr:
            for note in self.data:
                if note == del_el:
                    self.data.remove(note)
