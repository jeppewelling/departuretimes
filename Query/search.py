import math

L = u"Location"
LAT = u"Lat"
LON = u"Lon"

LAT_MIN = u'LatMin'
LAT_MAX = u'LatMax'

LON_MIN = u'LonMin'
LON_MAX = u'LonMax'

B = u'Bound'
D = u'Distance'

# Thanks to:
# http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates

MIN_LAT = math.radians(-90)  # -PI/2
MAX_LAT = math.radians(90)  # PI/2
MIN_LON = math.radians(-180)  # -PI
MAX_LON = math.radians(180)  # PI

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
        minLat = max(minLat, MIN_LAT)
        maxLat = min(maxLat, MAX_LAT)
        minLon = MIN_LON
        maxLon = MAX_LON

    return {B: {LAT_MIN: math.degrees(minLat),
                LON_MIN: math.degrees(minLon),
                LAT_MAX: math.degrees(maxLat),
                LON_MAX: math.degrees(maxLon)}}


def search(points, lat, lon, distance):
    approximate = approximate_search(points, lat, lon, distance)
    point_with_distance = map(lambda p:
                              add_distance_to_point(p, lat, lon),
                              approximate)
    return filter(lambda p:
                  distance >= p[D],
                  point_with_distance)


def add_distance_to_point(p, lat, lon):
    loc = p[L]
    distance_points = distance_between_points(lat,
                                              lon,
                                              loc[LAT],
                                              loc[LON])
    p.update({D: distance_points})
    return p


# Find the points within the square of the source point.
def approximate_search(points, lat, lon, distance):
    span = lon_span(lat, lon, distance)

    if span is None:
        return None

    return filter(lambda p:
                  is_point_nearby(p, span),
                  points)


def is_point_nearby(p, span):
    print "Point: %s" % p
    loc = p[L]
    if LAT not in loc:
        return False

    bound = span[B]
    lat = loc[LAT]
    lon = loc[LON]

    return bound[LAT_MAX] >= lat >= bound[LAT_MIN] \
           and bound[LON_MAX] >= lon >= bound[LON_MIN]


def get_lat(loc):
    if LAT in loc:
        return loc[LAT]
    return 0


def get_lon(loc):
    if LON in loc:
        return loc[LON]
    return 0


# Calculates the distance between the stations in the list: stations
# and the given point: lat, lon
# returns the stations that are within the given radius.
def get_stations_near(lat, lon, radius, stations):
    station_distances = map(lambda s:
                            {'Distance':
                                 distance_between_points(
                                     lat,
                                     lon,
                                     float(s['Location']['Lat']),
                                     float(s['Location']['Lon'])),
                             'Name': s['Name'],
                             'Uic': s['Uic']},
                            stations)
    print "B"
    return filter(
        lambda s: s['Distance'] <= radius,
        station_distances)


# Thanks to:
# http://andrew.hedges.name/experiments/haversine/
def distance_between_points(lat1, lon1, lat2, lon2):
    # mean radius of the earth (km) at 39 degrees from the equator
    Rk = 6373

    t1 = lat1
    n1 = lon1
    t2 = lat2
    n2 = lon2

    # convert coordinates to radians
    lat1 = deg2rad(t1)
    lon1 = deg2rad(n1)
    lat2 = deg2rad(t2)
    lon2 = deg2rad(n2)

    # find the differences between the coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # here's the heavy lifting
    a = math.pow(math.sin(dlat / 2), 2) + math.cos(lat1) * math.cos(lat2) * math.pow(math.sin(dlon / 2), 2)

    # great circle distance in radians
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # great circle distance in km
    km = c * Rk

    return km


def deg2rad(deg):
    rad = deg * math.pi / 180
    return rad
