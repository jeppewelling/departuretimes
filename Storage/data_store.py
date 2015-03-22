# -*- coding: utf-8 -*-


class DataStore(object):

    def __init__(self):
        self.stations_index = {}
        self.departures_index = {}
        self.stations_list = []

    # Returns a list of stations
    def get_stations(self):
        return self.stations_list

    # Returns a map from station id to list of departures
    def get_departures_from_stations(self, stations):
        departure_map = {}
        for s in stations:
            uic = s['Uic']
            if uic in self.departures_index:
                departures = self.departures_index[s['Uic']]
                # only return a mapping if any departures exist
                if departures:
                    departure_map[s['Uic']] = departures

        return departure_map


    def get_all_departures(self):
        return self.departures_index

    def add_to_departures_index(self, station_id, departures):
        self.departures_index[station_id] = departures

    def index_stations(self, stations):
        # Build an index of the stations for fast lookup
        for s in stations:
            self.stations_index[s['Uic']] = s

        self.stations_list = stations
