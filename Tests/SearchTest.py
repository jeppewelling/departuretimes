# -*- coding: utf-8 -*-
import codecs
import json
import unittest
from QueryDepartures.search import lat_lon_span, search


class TestSearch(unittest.TestCase):


    def setUp(self):
        self.places = None
        with codecs.open("./places.json", 'r') as f:
            self.places = json.load(f)


        f.close()

    def test_lon_span(self):
        sogenfri = {"Place": "Sorgenfri", "Location": {"Lat": 55.7812551, "Lon": 12.4835422}}
        location = sogenfri['Location']
        print lat_lon_span(location['Lat'], location['Lon'], 5)

    def test_lon_span(self):
        sogenfri = {"Place": "Sorgenfri", "Location": {"Location": {"Lat": 55.7812551, "Lon": 12.4835422}}}
        location = sogenfri['Location']['Location']
        self.assertEquals({u'Bound': {u'LatMax': 55.82622110971674, u'LonMin': 12.40358184612347, u'LonMax': 12.563502553876532, u'LatMin': 55.736289090283265}},
                          lat_lon_span(location['Lat'], location['Lon'], 5))



    def test_search(self):
        aarhus = {"Lat": 56.15016019999999, "Lon": 10.2040587}
        results = search(self.places, aarhus['Lat'], aarhus['Lon'], 5)
        self.assertEquals([{u'Distance': 0.6298185439652639, u'Place': u'Europaplads', u'Location': {u'Lat': 56.1533622, u'Lon': 10.212443}},
                           {u'Distance': 0.9194746264247469, u'Place': u'Skolebakken', u'Location': {u'Lat': 56.1567948, u'Lon': 10.2129122}},
                           {u'Distance': 3.4062595851405755, u'Place': u'Den Permanente', u'Location': {u'Lat': 56.1767208, u'Lon': 10.231433}},
                           {u'Distance': 0.0, u'Place': u'\xc5rhus H', u'Location': {u'Lat': 56.15016019999999, u'Lon': 10.2040587}},
                           {u'Distance': 1.6469894920248063, u'Place': u'\xd8stbanetorvet', u'Location': {u'Lat': 56.163275, u'Lon': 10.2164015}}],
                          results)





