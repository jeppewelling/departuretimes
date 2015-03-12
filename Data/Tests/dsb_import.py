import unittest
from Data.dsb_import import add_geo_locations_to_place,\
    add_geo_locations_to_places\
    import_stations
from Data.google_georesolver import GoogleGeoResolver


class TestDsbImport(unittest.TestCase):

    def setUp(self):
        return None

    def test_add_geo_locations_to_place(self):
        place = {'Name': "Sorgenfri", 'Country': "Denmark"}
        cache = {u'Denmark': {u'Sorgenfri': {u'Location':
                                             {u'Lat': 55.78263,
                                              u'Lon': 12.49044}},
                              u'Brejning': {u'Location':
                                            {u'Lat': 55.6647368,
                                             u'Lon': 9.673658699999999}},
                              u'Tarm': {u'Location':
                                        {u'Lat': 55.9066,
                                         u'Lon': 8.520292999999999}},
                              u'Knabstrup': {u'Location':
                                             {u'Lat': 55.664414,
                                              u'Lon': 11.552356}},
                              u'\xd8lgod': {u'Location':
                                            {u'Lat': 55.807331,
                                             u'Lon': 8.618423}},
                              u'Ordrup': {u'Location': {u'Lat': 55.763123,
                                                        u'Lon': 12.579436}}}}
        georesolver = GoogleGeoResolver()
        georesolver.cached_index = cache
        result = add_geo_locations_to_place(place, georesolver)
        self.assertEqual({'Name': "Sorgenfri",
                          'Country': "Denmark",
                          u"Location": {u'Lat': 55.78263,
                                        u'Lon': 12.49044}},
                         result)

    def test_add_geo_locations_to_data(self):
        places = [{'Name': "Sorgenfri", 'Country': "Denmark"}]
        cache = {u'Denmark': {u'Sorgenfri': {u'Location':
                                             {u'Lat': 55.78263,
                                              u'Lon': 12.49044}},
                              u'Brejning': {u'Location':
                                            {u'Lat': 55.6647368,
                                             u'Lon': 9.673658699999999}},
                              u'Tarm': {u'Location':
                                        {u'Lat': 55.9066,
                                         u'Lon': 8.520292999999999}},
                              u'Knabstrup': {u'Location':
                                             {u'Lat': 55.664414,
                                              u'Lon': 11.552356}},
                              u'\xd8lgod': {u'Location':
                                            {u'Lat': 55.807331,
                                             u'Lon': 8.618423}},
                              u'Ordrup': {u'Location': {u'Lat': 55.763123,
                                                        u'Lon': 12.579436}}}}
        georesolver = GoogleGeoResolver()
        georesolver.cached_index = cache
        result = add_geo_locations_to_places(places, georesolver)
        self.assertEqual([{'Name': "Sorgenfri",
                           'Country': "Denmark",
                           u"Location": {u'Lat': 55.78263,
                                         u'Lon': 12.49044}}],
                         result)


if __name__ == '__main__':
    unittest.main()
