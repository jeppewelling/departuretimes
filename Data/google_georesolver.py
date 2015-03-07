import json
from os.path import isfile
from json_url_import import import_json
from urllib import urlencode
import io

P = u'Place'
C = u'Country'
N = u'Name'
L = u'Location'
LAT = u'Lat'
LON = u'Lon'

api_url = "https://maps.googleapis.com/maps/api/geocode/json?%s"\
          "&key=AIzaSyBW43vhEDudt_ZEaIlF7-bBKPeSNGW9D-s"

places_file = "./data/places_location.json"


# A list of places: {Name: n, Country: c}
def main(list_of_places):
    # list_of_places = places_to_utf8(list_of_places)
    # First check if the locations are stored locally
    index_cache = read_places(places_file)

    # If the local cache is empty, fill it up
    if not index_cache:
        index = places_to_location_index(list_of_places)
        # save as local cache
        store_places(places_file, index)
        return index

    updated_index = fillout_missing_places(list_of_places, index_cache)
    store_places(places_file, updated_index)
    print updated_index
    return updated_index


# def places_to_utf8(list_of_places):
#     return map(lambda x:
#                as_place(toUtf8(x[N]),
#                         toUtf8(x[C])),
#                list_of_places)


# There might be places not found in the local cache
def fillout_missing_places(list_of_places, index):
    for p in list_of_places:
        country = toUtf8(p[C])
        name = toUtf8(p[N])
        if country not in index:
            index[country] = {name: location_from_place(p)}

        place_index = index[country]
        if name not in place_index:
            index[country][name] = location_from_place(p)

    return index


# Input: list of: {Name: n, Country: c}
# Output: dict of: {Country: {Name : {Location: {Lat: l, Lon: o}}}}
def places_to_location_index(places):
    # pairs of place, location
    pairs = map(bind_place_with_location, places)
    return index_addresses_by_place(pairs)


def bind_place_with_location(place):
    location = location_from_place(place)
    return {P: place,
            L: location}


def toUtf8(v):
    print v
    return v.decode('utf8')


def location_from_place(p):
    """ Input: a place: {Name: n, Country: c}, Returns a location object. """
    loc = location_from_google_place_info(
        resolve_place(p[N],
                      p[C]))

    print "Google georesolver: Searched for: %s, found: %s" % (p, loc)
    return loc


def resolve_place(place, country):
    """ Input: place, country. Returns the raw json from the google api. """
    address = "%s,%s" % (place, country)
    print address
    enc = urlencode({'address': address})
    url = api_url % enc
    return import_json(url)


def location_from_google_place_info(place_info):
    """Input: place_info, the raw json from the google api. Returns the location
    information as a dictionary."""
    results = place_info['results']
    if not results:
        return as_location(0, 0)

    location = results[0]['geometry']['location']
    return as_location(location['lat'], location['lng'])


def as_place(name, country):
    return {N: name,
            C: country}


def as_location(lat, lon):
    return {L: {LAT: lat,
                LON: lon}}


def store_places(file_path, place_locations):
    print place_locations
    with open(file_path, 'w') as f:
        json.dump(place_locations, f)
    f.close()


def read_places(file_path):
    if not isfile(file_path):
        return []

    try:
        with open(file_path, 'r') as f:
            addresses = json.load(f)
        f.close()
    except ValueError:
        return []
    return addresses


# Input: paris of place, location
def index_addresses_by_place(addresses):
    index = {}
    for address in addresses:
        country = toUtf8(address[P][C])
        name = toUtf8(address[P][N])
        location = address[L]

        if country not in index:
            index[country] = {name: location}
            continue

        places = index[country]
        # it is assmed that the places have unique names
        places[name] = location

    return index


# TODO: make an adapter: stations to places
#       


# if __name__ == "__main__":
#     print main("skolebakken st", "Denmark")
