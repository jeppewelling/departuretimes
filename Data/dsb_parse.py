# -*- coding: utf-8 -*-
# Parser for the DSB json
import pytz
import datetime

# Imports the list of departures from a given station.
# UIC -> list of <departure info>
def parse_departure_list(departures):
    return map(lambda x: 
                 # Common
               { 'DestinationName' : x['DestinationName'],
                 'DestinationId' : x['DestinationID'],

                 'Cancelled' : parse_boolean(x['Cancelled']),
                 'TrainType': x['TrainType'],
                 'Track' : x['Track'],
                 
                 # Fjern og Regional tog
                 'ScheduledDeparture' : parse_datetime(x['ScheduledDeparture']),
                 'DepartureDelayInSeconds' : parse_optional_number(x['DepartureDelay']),


                 # S-tog
                 'TimeGenerated' : parse_datetime(x['Generated']),
                 # Minutes after TimeGenerated
                 'MinutesToDeparture' : parse_minutes(x['MinutesToDeparture']),
                 'Direction' : x['Direction'] }, departures)


def datetime_str_to_int(str_datetime):
    return int(str_datetime.strip('/Date()'))/1000


def parse_optional_number(str_number):
    if str_number == None:
        return 0
    return int(str_number)


# string -> datetime
def parse_datetime(str_datetime):
    if str_datetime == None:
        return None

    # Convert the time to utc time
    parsed = datetime.datetime.fromtimestamp(datetime_str_to_int(str_datetime))
    local = pytz.timezone ("Europe/Copenhagen")
    local_dt = local.localize(parsed, is_dst=None)
    utc_dt = local_dt.astimezone (pytz.utc)
    return utc_dt

    # Seems like the time send to us by DSB has one hour added
    # We have set timezone to Europe / Copenhagen

    
# string -> boolean
def parse_boolean(str_boolean):
    if str_boolean == "True":
        return True
    return False


# Also handles half minutes.
# string -> float
def parse_minutes(str_minutes):
    if str_minutes == None:
        return 0
    if str_minutes == u'½':
        return 0.5
    try:
        return float(str_minutes)
    except Exception:
        print "Unable to convert: %s to a float." % str_minutes
        return 0
