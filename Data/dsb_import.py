# -*- coding: utf-8 -*-
import datetime
import calendar
import urllib
import urllib2
import rmq_send
from time import sleep
from dsb_parse import parse_departure_list
from json_url_import import import_json
from DepartureTimes.communication.interrupt_handler \
    import block_signals, exception_handler
from google_georesolver import GoogleGeoResolver, as_location_not_found


import_timeout_minutes = 5

dsb_url = "http://traindata.dsb.dk/stationdeparture/"\
          "opendataprotocol.svc"

dsb_queue_url = dsb_url + "/Queue()?$format=json&$filter="
dsb_stations_url = dsb_url + "/Station()?$format=json"


def main():
    #exception_handler(import_all)
    import_all()


def import_all():
    georesolver = GoogleGeoResolver()
    while True:
        with block_signals():
            dsb_import(georesolver)

            # Wait 5 minutes before importing again
            sleep(60 * import_timeout_minutes)


def get_station_query(station_id):
    query_station = "(StationUic eq '" + station_id + "')"
    return urllib.quote_plus(query_station)


# datetime * minutes -> datetime
def add_minutes(dt, m):
    seconds = m * 60
    return dt + datetime.timedelta(seconds=seconds)


def add_seconds(dt, s):
    return dt + datetime.timedelta(seconds=s)


# Imports the list of departures from a given station.
# UIC -> list of <departure info>
def import_departures_from_station(station_id):
    q = get_station_query(station_id)
    url = dsb_queue_url + q
    raw_json = import_json(url)
    return unify_stog_and_regional(
        parse_departure_list(raw_json['d']))



# The S-togs arrival times are given as a time and an offset,
# We want to unify this with the Regional trains who has a
# Scheduled departure time.
def unify_stog_and_regional(departures):
    return map(unify_departure, departures)


def strip_unused_fields_and_update_scheduleddeparture(
        departure,
        departure_time):
    return {'DestinationName': departure['DestinationName'],
            'DestinationId': departure['DestinationId'],

            'Cancelled': departure['Cancelled'],
            'TrainType': departure['TrainType'],
            'Track': departure['Track'],
            'Type': 'Train',

            # A calculated departure time (considers delay and
            # unifies regional trains with s-trains) Convert
            # DepartureTime to Unix time stamp
            'DepartureTime': calendar.timegm(departure_time.utctimetuple()),

            # S-tog
            'Direction': departure['Direction']}


# list of departures -> unified list of departures
def unify_departure(departure):
    # if scheduled departure is none, we have to add the
    # MinutesToDeparture to TimeGenerated.
    if departure['ScheduledDeparture'] == None:
        return strip_unused_fields_and_update_scheduleddeparture(
            departure,
            add_minutes(
                departure['TimeGenerated'],
                departure['MinutesToDeparture']))

    # For regional trains there is a property called DepartureDaley
    # (in seconds) to have the proper departure time, we add the delay
    # to the secheduled departure.
    return strip_unused_fields_and_update_scheduleddeparture(
        departure,
        add_seconds(
            departure['ScheduledDeparture'],
            departure['DepartureDelayInSeconds']))


# Imports a list of stations:
# georesolver -> list of { Country, UIC, Name}
def import_stations(georesolver):
    raw_json = import_json(dsb_stations_url)
    lst = raw_json['d']

    # Convert the raw data to a sub set of the data we are interested in.
    converted_data = map(convert_to_place, lst)

    # Add geo locations to data
    return add_geo_locations_to_places(converted_data, georesolver)


def add_geo_locations_to_places(places, georesolver):
    georesolver.fetch_place_to_location_map(places)
    return map(lambda p:
               add_geo_locations_to_place(p, georesolver),
               places)


def add_geo_locations_to_place(place, georesolver):
    with block_signals():
        location = georesolver.lookup_place(place)
        if not location:
            location = as_location_not_found()

        place.update(location)
        return place


# Input: S, station
def convert_to_place(s):
    return {u"Country": countryname_to_country(s['CountryName']),
            u"Uic": s['UIC'],
            u"Name": s['Name']}


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


def dsb_import_departures_from_stations(stations):
    for station in stations:
        with block_signals():
            try:
                rmq_send.send_departures_to_storage(
                    station,
                    import_departures_from_station(
                        station['Uic']))
            except (urllib2.HTTPError, urllib2.URLError):
                print "Connection error when trying to retrieve departures from station: %s" % station

        # Lets not ddos DSB :-)
        sleep(2)


# see more at:
# http://www.dsb.dk/dsb-labs/webservice-stationsafgange/
def dsb_import(georesolver):
    print "Importing stations from DSB..."
    stations = import_stations(georesolver)
    print "Found %r stations." % (len(stations))

    print "Transmitting data to storage service..."
    rmq_send.send_stations_to_storage(stations)

    # Import departures from each station
    dsb_import_departures_from_stations(stations)


if __name__ == "__main__":
    print import_departures_from_station("7401543")
