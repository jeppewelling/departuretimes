import unittest
from Data.google_georesolver import GoogleGeoResolver, to_unicode


class TestGoogleGeoresolver(unittest.TestCase):

    def setUp(self):
        return None

    def test_add_geo_locations_to_place(self):
        resolver = GoogleGeoResolver()
        places = [{u'Name': to_unicode("Østbanetorvet"),
                   u'Country': u'Denmark'},
                  {u'Name': to_unicode("Tårnby"),
                   u'Country': u'Denmark'}]

        index = resolver.fetch_place_to_location_map(places)
        self.assertEqual(index[u'Denmark'][to_unicode("Østbanetorvet")],
                         {u'Location':
                          {u'Lat': 56.1636965, u'Lon': 10.2149822}})
        self.assertEqual(index[u'Denmark'][to_unicode("Tårnby")],
                         {u'Location':
                          {u'Lat': 55.62551999999999, u'Lon': 12.594765}})


if __name__ == '__main__':
    unittest.main()
