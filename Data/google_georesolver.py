import json
from json_url_import import import_json
from urllib import urlencode


api_url = "https://maps.googleapis.com/maps/api/geocode/json?%s"\
          "&key=AIzaSyBW43vhEDudt_ZEaIlF7-bBKPeSNGW9D-s"


def main(address, country):
    return location_from_place(
        resolve_place(address, country))


# Input: list of: {Name: n, Country: c}
# Output: list of: {Place: {Name: a, Country: c},
#                   Location: {Lat: l, Lon: o}}
def resolve_list_of_places(places):
    return map(bind_place_with_location, places)


def bind_place_with_location(place):
    name = place['Name']
    country = place['Country']
    location = location_from_place(
        resolve_place(name, country))

    out = {'Place': place}
    out.update(location)
    return out


def resolve_place(place, country):
    address = "%s,%s" % (place, country)
    enc = urlencode({'address': address})
    url = api_url % enc
    return import_json(url)


def location_from_place(place_info):
    results = place_info['results']
    if not results:
        return as_location(0, 0)

    location = results[0]['geometry']['location']
    return as_location(location['lat'], location['lng'])


def as_place(name, country):
    return {'Name': name, 'Country': country}


def as_location(lat, lon):
    return {'Location': {'Lat': lat, 'Lon': lon}}


def store_places(file_path, place_locations):
    with open(file_path, 'w') as f:
        json.dump(place_locations, f)
    f.close()


def read_places(file_path):
    with open(file_path, 'r') as f:
        addresses = json.load(f)
    f.close()
    return addresses


def index_addresses_by_place(addresses):
    index = {}
    for address in addresses:
        country = address['Place']['Country']
        name = address['Place']['Name']
        location = address['Location']

        if country not in index:
            index[country] = {name: location}
            continue

        places = index[country]
        # it is assmed that the places have unique names
        places[name] = location

    return index


# TODO: make an adapter: stations to places
#       check if location file is already stored
#       

if __name__ == "__main__":
    print main("skolebakken st", "Denmark")
