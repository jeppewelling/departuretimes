# -*- coding: utf-8 -*-
from Storage.data_store import DataStore, get_city_by_name
import unittest

class TestDataStore(unittest.TestCase):

    def setUp(self):
        return None

    def test_empty_store(self):
        store = DataStore()
        self.assertEqual([], store.get_stations())

        # if the city list is empty, the result of calling
        # get_stations is an empty list, since the city list is
        # required for geo - locations.
    def test_empty_city_list(self):
        store = DataStore()
        stations = []
        stations.append({"Name" : "Foo",
                         "Country" : "DK",
                         "Uic" : "42"})

        stations.append({"Name" : "Bar",
                         "Country" : "DK",
                         "Uic" : "7"})

        stations.append({"Name" : "Baz",
                         "Country" : "DK",
                         "Uic" : "22"})

        store.index_stations(stations)
        self.assertEqual([], store.get_stations())

    def test_stations_and_city_list(self):
        store = DataStore()
        stations = []
        stations.append({"Name" : "Foo",
                         "Country" : "DK",
                         "Uic" : "42"})

        stations.append({"Name" : "Bar",
                         "Country" : "DK",
                         "Uic" : "7"})

        stations.append({"Name" : "Baz",
                         "Country" : "DK",
                         "Uic" : "22"})

        cities = []
        cities.append({"Name" : "Foo",
                       "Lat" : 1,
                       "Lon" : 2})

        cities.append({"Name" : "Bar",
                       "Lat" : 3,
                       "Lon" : 4})

        cities.append({"Name" : "Baz",
                       "Lat" : 5,
                       "Lon" : 6})

        asserted_result = []
        asserted_result.append({"Name" : "Foo",
                                "Country" : "DK",
                                "Uic" : "42",
                                "Lat" : 1,
                                "Lon" : 2})

        asserted_result.append({"Name" : "Bar",
                                "Country" : "DK",
                                "Uic" : "7",
                                "Lat" : 3,
                                "Lon" : 4})


        asserted_result.append({"Name" : "Baz",
                                "Country" : "DK",
                                "Uic" : "22",
                                "Lat" : 5,
                                "Lon" : 6})

        store.index_stations(stations)
        store.index_cities(cities)
        self.assertEqual(asserted_result, store.get_stations())


    def test_city_matching(self):
        store = DataStore()
        cities = []
        cph = {"Name" : "København",
                       "Lat" : 1,
                       "Lon" : 2}
        cities.append(cph)

        cities.append({"Name" : "Bar",
                       "Lat" : 3,
                       "Lon" : 4})

        cities.append({"Name" : "Baz",
                       "Lat" : 5,
                       "Lon" : 6})
        store.index_cities(cities)

        # Finds copenhagen from a name almost the same
        city = get_city_by_name("Kæbenhavn H", store.get_cities())
        self.assertEqual(cph, city)

if __name__ == '__main__':
    unittest.main()
