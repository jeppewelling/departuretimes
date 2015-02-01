# -*- coding: utf-8 -*-

import urllib2
import json
import urllib
import datetime
import rmq_send
import calendar
from city_location_import import import_cities_from_csv
from dsb_parse import parse_departure_list

dsb_queue_url = "http://traindata.dsb.dk/stationdeparture/opendataprotocol.svc/Queue()?$format=json&$filter="
dsb_stations_url = "http://traindata.dsb.dk/stationdeparture/opendataprotocol.svc/Station()?$format=json"


# Imports json from a given url.
def import_json(url):
    response = urllib2.urlopen(url)
    raw_departures = response.read()
    return json.loads(raw_departures)


def get_station_query(station_id):
    query_station = "(StationUic eq '"+ station_id + "')"
    return urllib.quote_plus(query_station)

    
# datetime * minutes -> datetime
def add_minutes(dt, m):
    seconds = m * 60
    return dt + datetime.timedelta(seconds = seconds)
    

def add_seconds(dt, s):
    return dt + datetime.timedelta(seconds = s)


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


def strip_unused_fields_and_update_scheduleddeparture(departure, departure_time):
    return { 'DestinationName' : departure['DestinationName'],
             'DestinationId' : departure['DestinationId'],
             
             'Cancelled' : departure['Cancelled'],
             'TrainType': departure['TrainType'],
             'Track' : departure['Track'],
             
             # A calculated departure time (considers delay and
             # unifies regional trains with s-trains)
             # Convert DepartureTime to Unix time stamp
             'DepartureTime' : calendar.timegm(departure_time.utctimetuple()),
             
             # S-tog
             'Direction' : departure['Direction'] }


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
#  Country
#  UIC (station id)
#  Name
# () -> list of { Country, UIC, Name}
def import_stations():
    raw_json = import_json(dsb_stations_url)
    lst = raw_json['d']
    return map(lambda x: 
               { "Country" : x['CountryName'], 
                 "Uic" : x['UIC'],
                 "Name" : x['Name'].encode("utf-8") }, lst)


# see more at:
# http://www.dsb.dk/dsb-labs/webservice-stationsafgange/
if __name__ == "__main__":
    city_location_data = "DataImport/data/GeoLiteCity-Location.csv"    
    
    print "Importing stations from DSB..."
    stations = import_stations()
    print "Found %r stations." % (len(stations))

    print "Importing citites from csv file..."
    cities = import_cities_from_csv(city_location_data)
    print "Found %r cities." % (len(cities))

    print "Transmitting data to storage service..."
    rmq_send.send_stations_to_storage(stations)
    rmq_send.send_cities_to_storage(cities)

    for station in stations:
        name = station['Name']
        #print "Station: %r" % name
        if name == "Hadsten" \
        or name == "København H":
        
            print "Departures from: %s" % station
            rmq_send.send_departures_to_storage(
                station,
                import_departures_from_station(
                    station['Uic']))



