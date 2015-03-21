import json
import time
from DepartureTimes.communication.rpc_server import RpcServer
from DepartureTimes.communication.queues import \
    query_queue_name, \
    storage_query_queue_name

from DepartureTimes.communication.interrupt_handler import exception_handler
from Health.health import \
    health_check_search_time, \
    health_check_fetch_stations, \
    health_check_fetch_departures
from search_optimal import search
from DepartureTimes.communication.rpc_client import RpcClient


def main():
    #exception_handler(setup)
    setup()


def setup():
    query_service = QueryService()
#    query_service.fetch_stations_from_storage()

    server = RpcServer(query_queue_name, query_service)
    server.start_consuming()


# Handles the request by the web client
class QueryService(object):
    def __init__(self):
        self.stations_cache = []

    # Fetches the stations from the storage, this information is
    # pretty static so only call this once.
    def fetch_stations_from_storage(self):
        # The stations are returned as a mapping from station id
        # to stations, lets convert it into a list for the search
        # algorithm.
        start = time.time()
        self.stations_cache = storage_query_get_stations()
        end = time.time()
        health_check_fetch_stations(end - start)

    def on_message_received(self, request):
        # If no statios were found in the cache, read from the store
        
        # if not self.stations_cache:
        #     self.fetch_stations_from_storage()

        print "message received: %s" % request
        request = json.loads(request)
        lat = float(request['Lat'])
        lon = float(request['Lon'])
        radius = float(request['RadiusKm'])

        start = time.time()
        stations_near_by = search(self.stations_cache, lat, lon, radius)
        end = time.time()
        health_check_search_time(end - start)

        print "stations near by: %s" % stations_near_by

        # Get departures for local stations.  Stations with no departures
        # are weeded out, thus there is no guarantee that there is a
        # mapping for each local station.
        start = time.time()
        # TODO add timeout
        departures = storage_query_get_departures(stations_near_by)
        end = time.time()
        health_check_fetch_departures(end - start)

        print "storage_query_get_departures time: %s seconds." % (end - start)
        print ""

        departures_added_name = map_stations_to_departures(stations_near_by,
                                                           departures)
        
        return json.dumps(make_result(lat,
                                      lon,
                                      departures_added_name))


# Input: list of: local_stations,
#        dict of: Uic -> departures
# Output: list of: {Uic, StationName, Departures, Distance, Location}
# (see output_information)
def map_stations_to_departures(local_stations, departures):
    out = []
    for station in local_stations:
        uic = station['Uic']
        # There might not be a mapping for each local station to a
        # list of departures
        if uic in departures:
            departures_from_station = departures[uic]
            out.append(output_information(station,
                                          departures_from_station,
                                          uic))
    return out


# Define the final output of the search function
def output_information(station, departures_from_station, uic):
    return {"Uic": uic,
            "StationName": station['Name'],
            "Departures": departures_from_station,
            "Distance": station['Distance'],
            "Location": station['Location']}


# Wraps the result to be returned to the client
def make_result(lat, lon, result):
    res = {}
    res['request'] = {'lat': lat, 'lon': lon}
    res['result'] = result
    return result


# input: dictionary of: station_id -> station
# output: list of stations
# def to_list(station_index):
#     out = []
#     for i, station in station_index.iteritems():
#         out.append(station)
#     return out


# Used to read from the storage
rpcClient = RpcClient(storage_query_queue_name)


def storage_query_get_stations():
    q = {}
    q['type'] = "get_stations"
    return json.loads(rpcClient.call(json.dumps(q)))


def storage_query_get_departures(stations):
    q = {}
    q['type'] = "get_departures"
    q['data'] = stations
    return json.loads(rpcClient.call(json.dumps(q)))
