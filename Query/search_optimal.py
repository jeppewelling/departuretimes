import time
import math
from search import distance_between_points, get_stations_near

L = u"Location"
LAT = u"Lat"
LON = u"Lon"

LAT_MIN = u'LatMin'
LAT_MAX = u'LatMax'

LON_MIN = u'LonMin'
LON_MAX = u'LonMax'

B = u'Bound'

# Thanks to:
# http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates

MIN_LAT = math.radians(-90)   # -PI/2
MAX_LAT = math.radians(90)    # PI/2
MIN_LON = math.radians(-180)  # -PI
MAX_LON = math.radians(180)   # PI

EARTH_RADIUS_KM = 6371.01


# Returns the coordinates of the square surrounding the circle defined
# by the point (lat, lon), distance, where distance is the radius of
# the circle.
def lon_span(lat, lon, distance):
    radius = EARTH_RADIUS_KM
    if radius < 0 or distance < 0:
        return None

    radLat = math.radians(lat)
    radLon = math.radians(lon)

    # angular distance in radians on a great circle
    radDist = distance / radius

    minLat = radLat - radDist
    maxLat = radLat + radDist

    minLon = 0
    maxLon = 0
    if minLat > MIN_LAT and maxLat < MAX_LAT:
        deltaLon = math.asin(math.sin(radDist) / math.cos(radLat))
        minLon = radLon - deltaLon

        if minLon < MIN_LON:
            minLon += 2 * math.pi

        maxLon = radLon + deltaLon
        if maxLon > MAX_LON:
            maxLon -= 2 * math.pi
    else:
        # a pole is within the distance
        minLat = math.max(minLat, MIN_LAT)
        maxLat = math.min(maxLat, MAX_LAT)
        minLon = MIN_LON
        maxLon = MAX_LON

    return {B: {LAT_MIN: math.degrees(minLat),
                LON_MIN: math.degrees(minLon),
                LAT_MAX: math.degrees(maxLat),
                LON_MAX: math.degrees(maxLon)}}


def search(points, lat, lon, distance):
    approximate = approximate_search(points, lat, lon, distance)
    return filter(lambda p:
                  is_point_within_range(p, lat, lon, distance),
                  approximate)


def is_point_within_range(p, lat, lon, distance):
    loc = p[L]
    return distance >= distance_between_points(lat,
                                               lon,
                                               loc[LAT],
                                               loc[LON])


# Find the points within the square of the source point.
def approximate_search(points, lat, lon, distance):
    span = lon_span(lat, lon, distance)
    return filter(lambda p:
                  is_point_nearby(p, span),
                  points)


def is_point_nearby(p, span):
    loc = p[L]
    if LAT not in loc:
        return False

    bound = span[B]

    lat = loc[LAT]
    lon = loc[LON]

    return lat <= bound[LAT_MAX] \
        and lat >= bound[LAT_MIN] \
        and lon <= bound[LON_MAX] \
        and lon >= bound[LON_MIN]


def get_lat(loc):
    if 'Lat' in loc:
        return loc['Lat']
    return 0


def get_lon(loc):
    if 'Lon' in loc:
        return loc['Lon']
    return 0
 

def test():
    from Data.google_georesolver import read_places
    places_indexed = read_places("./places_location.json")

    out = []
    for country, places in places_indexed.iteritems():
        for place, location in places.iteritems():
            out.append({'Name': place,
                        'Country': country,
                        'Location': location['Location'],
                        'Lat': get_lat(location['Location']),
                        'Lon': get_lon(location['Location']),
                        'Uic': 42})

    lat = 56.1500
    lon = 10.2167
    distance = 15

    start = time.time()
    result = search(out, lat, lon, distance)
    end = time.time()

    for r in result:
        print r

    print "New: Execution time: %s seconds." % (end - start)

    start = time.time()
    old_resul = get_stations_near(lat, lon, distance, out)
    end = time.time()

    for r in old_resul:
        print r
    print "Old: Execution time: %s seconds." % (end - start)


if __name__ == "__main__":
    test()
