#!/usr/bin/env python
import json
from search import get_stations_near
import time


from DepartureTimes.communication.interrupt_handler import exception_handler
from DepartureTimes.communication.rpc_server import RpcServer
from read_from_storage import \
    storage_query_get_stations, \
    storage_query_get_departures
from DepartureTimes.communication.queues import query_queue_name


def main():
#    exception_handler(setup)
    setup()


def setup():
    server = RpcServer(query_queue_name, QueryServiceHandler())
    server.start_consuming()


# Wraps the result to be returned to the client
def make_result(lat, lon, result):
    res = {}
    res['request'] = {'lat': lat, 'lon': lon}
    res['result'] = result
    return result


# input: dictionary of: station_id -> station
# output: list of stations
def to_list(station_index):
    out = []
    for i, station in station_index.iteritems():
        out.append(station)
    return out


# Handles the request by the web client
class QueryServiceHandler(object):
    def __init__(self):
        self.stations_cache = []

    def on_message_received(self, request):
        request = json.loads(request)
        lat = float(request['Lat'])
        lon = float(request['Lon'])
        radius = float(request['RadiusKm'])

        # Get the entire list of stations to search for the losest one It
        # is a bit naive to just get the entire list, but the idea is to
        # seperate responsibility. The store only stores data and the
        # QueryHandler does the calculations.

        start = time.time()
        if not self.stations_cache:
            # The stations are returned as a mapping from station id
            # to stations, lets convert it into a list for the search
            # algorithm.
            print "requesting stations..."
            self.stations_cache = to_list(storage_query_get_stations())
        end = time.time()
        print "storage_query_get_stations time: %s seconds." % (end - start)
        print ""

        # Currently returns the stations near by, but should also return
        # departures for each stataion
        start = time.time()
        from search_optimal import search

        ## TODO deprecate get_stations_near
        # stations_near_by = get_stations_near(
        #     lat, lon, radius, self.stations_cache)
        stations_near_by = search(self.stations_cache, lat, lon, radius)
        end = time.time()

        print "get_stations_near time: %s seconds." % (end - start)
        print ""

        # Get departures for local stations.  Stations with no departures
        # are weeded out, thus there is no guarantee that there is a
        # mapping for each local station.
        start = time.time()
        departures = storage_query_get_departures(stations_near_by)
        end = time.time()
        print "storage_query_get_departures time: %s seconds." % (end - start)
        print ""

        departures_added_name = add_from_name_to_departures(stations_near_by,
                                                            departures)

        return json.dumps(make_result(lat,
                                      lon,
                                      departures_added_name))


def add_from_name_to_departures(local_stations, departures):
    out = []
    for station in local_stations:
        uic = station['Uic']
        # There might not be a mapping for each local station to a
        # list of departures
        if uic in departures:
            departures_from_station = departures[uic]
            out.append(append_from_station_name(station,
                                                departures_from_station,
                                                uic))
    return out


def append_from_station_name(station, departures_from_station, uic):
    return {"Uic": uic,
            "StationName": station['Name'],
            "Departures": departures_from_station}





