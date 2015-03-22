from time import sleep
import json
import codecs
from os.path import isfile
import urllib
from json_url_import import import_json
from urllib import urlencode

P = u'Place'
C = u'Country'
N = u'Name'
L = u'Location'
LAT = u'Lat'
LON = u'Lon'
M = u'Message'

api_url = "https://maps.googleapis.com/maps/api/geocode/json?%s"\
          "&key=AIzaSyBW43vhEDudt_ZEaIlF7-bBKPeSNGW9D-s"

places_file = "./places_location.json"


class GoogleGeoResolver(object):
    def __init__(self):
        self.cached_index = {}

    def fetch_place_to_location_map(self, list_of_places):
        # First check if the locations are stored locally
        self.cached_index = read_places(places_file)

        # Ensure that new places are added to the index and georesolved
        self.cached_index = fillout_missing_places(list_of_places,
                                                   self.cached_index)

        store_places(places_file, self.cached_index)
        return self.cached_index

    def lookup_place(self, place):
        country = place[C]
        name = place[N]
        if country not in self.cached_index:
            return as_location_not_found()

        if name not in self.cached_index[country]:
            return as_location_not_found()

        return self.cached_index[country][name]


# A list of places: {Name: n, Country: c}
# def main(list_of_places):
#     # list_of_places = places_to_utf8(list_of_places)
#     # First check if the locations are stored locally
#     index_cache = read_places(places_file)

#     updated_index = fillout_missing_places(list_of_places, index_cache)
#     store_places(places_file, updated_index)
#     return updated_index


# Georesolves the elements of the list: list_of_places that are not
# already found in the cached index.
#
# Input:
#  list_of_places:
#  list of: {Name: n, Country: c},
#
#  cached_index:
#  dict of: {Country: {Place: {Location: {Lat: l, Lon: o}}}}
#
# Output:
#  dict of: {Country: {Place: {Location: {Lat: l, Lon: o}}}}
def fillout_missing_places(list_of_places, cached_index):
    for p in list_of_places:
        country = p[C]
        place_name = p[N]
        if country not in cached_index:
            cached_index[country] = {place_name: location_from_place(p)}

        place_index = cached_index[country]
        if place_name not in place_index:
            cached_index[country][place_name] = location_from_place(p)

    return cached_index


def location_from_place(p):
    """ Input: a place: {Name: n, Country: c}, Returns a location object. """
    loc = location_from_google_place_info(
        resolve_place(p[N],
                      p[C]))


    print "Google georesolver: Searched for: %s, found: %s" % (p, loc)
    return loc


def resolve_place(place, country):
    if not place.lower().endswith(" st"):
        place_st = place + " st"

    res = resolve_place_helper(place_st, country)

    # try again without st
    if not res['results']:
        res = resolve_place_helper(place, country)

    return res


def resolve_place_helper(place, country):
    """ Input: place, country. Returns the raw json from the google api. """

    # Google allows for 5 request per second, 2500 requests per 24
    # hour. The max requests per 24 hour is not checked!
    sleep(0.2)

    address = u"%s,%s" % (place, country)
    address = address.encode('utf8')

    enc = urlencode({'address': address})
    url = api_url % enc
    return import_json(url)




def location_from_google_place_info(place_info):
    """Input: place_info, the raw json from the google api. Returns the location
    information as a dictionary."""
    results = place_info['results']
    if not results:
        return as_location_not_found()

    #location = results[0]['geometry']['location']
    location = first_or_train_type(results)
    return as_location(location['lat'], location['lng'])


def first_or_train_type(results):
    for r in results:
        address_components = r['address_components']
        for a in address_components:
            types = a['types']
            for t in types:
                if t == "train_station":
                    return r['geometry']['location']

    return results[0]['geometry']['location']




def as_place(name, country):
    return {N: name,
            C: country}


def as_location(lat, lon):
    return {L: {LAT: lat,
                LON: lon}}


def as_location_not_found():
    return {L: {M: "Location not available."}}


def store_places(file_path, place_locations):
    with open(file_path, 'w') as f:
        json.dump(place_locations, f)
    f.close()


def read_places(file_path):
    if not isfile(file_path):
        print "No file found for place locations at: %s." % file_path
        return {}
    try:
        with codecs.open(file_path, 'r') as f:
            places = json.load(f)
        f.close()
    except ValueError as ex:
        print "Unable to parse json file: %s" % ex
        return {}
    return places


# Input: paris of place, location
def index_addresses_by_place(addresses):
    index = {}
    for address in addresses:
        country = address[P][C]
        name = address[P][N]
        location = address[L]

        if country not in index:
            index[country] = {name: location}
            continue

        places = index[country]
        # it is assmed that the places have unique names
        places[name] = location

    return index
