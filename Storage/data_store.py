# -*- coding: utf-8 -*-


class DataStore(object):

    def __init__(self):
        self.stations_index = {}
        self.departures_index = {}

    # Return the stations with their geographical location appended
    def get_stations(self):
        return self.stations_index

    # Returns a map from station id to list of departures
    def get_departures_from_stations(self, stations):
        departure_map = {}
        for s in stations:
            uic = s['Uic']
            if uic in self.departures_index:
                departure_map[s['Uic']] = self.departures_index[s['Uic']]

        return departure_map

    # Returns a copty of the city index
    def get_cities(self):
        return dict(self.cities_index)

    def get_location_from_station_name(self, name):
        cities = self.get_cities()
        city = get_city_by_name(name, cities)
        if city is None:
            return None
        return city

    def add_to_departures_index(self, station_id, departures):
        self.departures_index[station_id] = departures

    def index_stations(self, stations):
        for s in stations:
            self.stations_index[s['Uic']] = s



# Helpers for making station names match with the city names
def remove_end_word(string, endword):
    if string.endswith(endword):
        return string[:-len(endword)]
    return string


# For better comparing citeies between the geolocation index and the
# station list from DSB
def remove_special_chars(city_name):
    return ''.join([i if ord(i) < 128 else ' ' for i in city_name])


def strip_from_city_name(city_name):
    city_name = remove_end_word(city_name, " Central")
    city_name = remove_end_word(city_name, " C")
    city_name = remove_end_word(city_name, " H")
    return city_name.strip()


# looks up a city by name, if no exact match is found, tries a sub match
def get_city_by_name(name, cities):
    try:
        return cities[name]
    except KeyError:
        return match_part_of_name(name, cities)


def transform_stations(s, cities):
    name = s['Name']
    city = get_city_by_name(name, cities)

    if city is None:
        return None
    return transform(city, s)


def transform(city, station):
    return {'Country': station['Country'],
            'Uic': station['Uic'],
            'Name': station['Name'],
            'Lat': city['Lat'],
            'Lon': city['Lon']}


def match_part_of_name(name, cities):
    name = strip_from_city_name(name)

    for key in cities:
        try:
            city = cities[key]
            c_name = remove_special_chars(city['Name'])
            name = remove_special_chars(name)
            if name in c_name:

                return city
        except KeyError:
            return None

    return None
