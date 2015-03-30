# coding=utf-8
import unittest

from Data.google_georesolver import GoogleGeoResolver


class TestGoogleGeoresolver(unittest.TestCase):

    def setUp(self):
        return None

    def test_add_geo_locations_to_place(self):
        resolver = GoogleGeoResolver()
        places = [{u'Name': u"Østbanetorvet",
                   u'Country': u'Denmark'},
                  {u'Name': u"Tårnby",
                   u'Country': u'Denmark'}]

        index = resolver.fetch_place_to_location_map(places)
        self.assertEqual(index[u'Denmark'][u"Østbanetorvet"],
                         {u'Location':
                          {u'Lat': 56.163275, u'Lon': 10.2164015}})
        self.assertEqual(index[u'Denmark'][u"Tårnby"],
                         {u'Location':
                          {u'Lat': 55.6299472, u'Lon': 12.602095}})




# Thanks to to
# https://writeonly.wordpress.com/2008/12/10/the-hassle-of-unicode-and-getting-on-with-it-in-python/
# It is not clear what encoding the input data are in, so we use this
# function to convert to utf8.
def to_unicode(str, verbose=False):
    '''attempt to fix non uft-8 string into utf-8, using a limited set of
    encodings'''

    # fuller list of encodings at
    # http://docs.python.org/library/codecs.html#standard-encodings
    if not str:
        return u''
    u = None
    # we could add more encodings here, as warranted.
    encodings = ('ascii', 'utf8', 'latin1')
    for enc in encodings:
        if u:
            break
        try:
            u = unicode(str, enc)
        except UnicodeDecodeError:
            if verbose:
                print "error for %s into encoding %s" % (str, enc)
            pass
    if not u:
        u = unicode(str, errors='replace')
        if verbose:
            print "using replacement character for %s" % str
    return u


def countryname_to_country(country_name):
    if country_name == "S":
        return u"Sweden"
    if country_name == "DK":
        return u"Denmark"
    return ""


