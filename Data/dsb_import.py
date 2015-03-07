# -*- coding: utf-8 -*-
import datetime
import rmq_send
import calendar
import urllib
from time import sleep
from city_location_import import import_cities
from dsb_parse import parse_departure_list
from json_url_import import import_json
from DepartureTimes.communication.interrupt_handler \
    import block_signals, exception_handler

import_timeout_minutes = 5

dsb_url = "http://traindata.dsb.dk/stationdeparture/"\
          "opendataprotocol.svc"

dsb_queue_url = dsb_url + "/Queue()?$format=json&$filter="
dsb_stations_url = dsb_url + "/Station()?$format=json"
def main():
    exception_handler(import_all)


def import_all():
    while True:
        with block_signals():
            dsb_import()

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


# Impors the list of departures from a given station.
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

            # A calculated departure time (considers delay and
            # unifies regional trains with s-trains) Convert
            # DepartureTime to Unix time stamp
            'DepartureTime': calendar.timegm(departure_time.utctimetuple()),

            # S-tog
            'Direction': departure['Direction']}


# list of departures -> unified list of departures
def unify_departure(departure):
    # if scheduled arrival is none, we have to add the
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
# () -> list of { Country, UIC, Name}
def import_stations():
    raw_json = import_json(dsb_stations_url)
    lst = raw_json['d']
    return map(lambda x:
               {"Country": x['CountryName'],
                "Uic": x['UIC'],
                "Name": x['Name'].encode("utf-8")}, lst)


# see more at:
# http://www.dsb.dk/dsb-labs/webservice-stationsafgange/
def dsb_import():
    print "Importing stations from DSB..."
    stations = import_stations()
    print "Found %r stations." % (len(stations))

    print "Importing citites from csv file..."
    cities = import_cities()
    print "Found %r cities." % (len(cities))

    print "Transmitting data to storage service..."
    rmq_send.send_stations_to_storage(stations)
    rmq_send.send_cities_to_storage(cities)

    for station in stations:
        with block_signals():
            rmq_send.send_departures_to_storage(
                station,
                import_departures_from_station(
                    station['Uic']))

        # Lets not ddos DSB :-)
        sleep(2)
