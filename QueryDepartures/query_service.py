import json

from DepartureTimes.communication.health_client_rmq import HealthClient
from DepartureTimes.communication.interrupt_handler import exception_handler
from DepartureTimes.communication.queues import query_queue_name
from DepartureTimes.communication.rpc_client import RpcClient
from QueryDepartures.setup_rmq import RmqSetup
from search import search


def main():
    exception_handler(setup)
    #setup()


# The public entry to searching
# Posts an entry in the search queue: "query_queue"
rpc = RpcClient(query_queue_name)
health = HealthClient()
def find_departures(lat, lon, radius):
    health.begin_search_time_measure()
    result = find_departures_no_health_logging(lat, lon, radius)
    health.end_search_time_measure()
    return result

def find_departures_no_health_logging(lat, lon, radius):
    return json.loads(rpc.call(encode_message(lat, lon, radius)))

def encode_message(lat, lon, radius):
    req = {'Lat': lat, 'Lon': lon, 'RadiusKm': radius}
    return json.dumps(req)


# setup the RMQ subscription / RPC
def setup():
    query_service = QueryService()
    rmq = RmqSetup(query_service)


    # On startup read all stations and departures from the storage.
    print " [QueryDepartures] Fetching initial state from storage..."
    rmq.fetch_stations_from_storage()
    rmq.fetch_all_departures_from_storage()

    print " [QueryDepartures] Initial state fetched. Ready for queries."
    # start listening on the messages published by the storage
    rmq.start_listening()


def as_subscription(e, m):
    return {'ExchangeName': e, 'MessageHandler': m}


def as_rpc(e, m):
    return {'QueueName': e, 'MessageHandler': m}



# Handles the request from the web client
# Maintains a local cache of the storage (is continuously updated by the storage)
class QueryService(object):
    def __init__(self):
        self.stations_cache = []
        self.departures = {}

    def get_stations(self):
        return self.stations_cache

    # Input: dict of: Uic -> list of departures
    # Called when a departure is published from the storage
    def update_departures(self, departures_from_single_station):
        if departures_from_single_station == "": return
        parsed = json.loads(departures_from_single_station)
        self.departures.update(parsed)

    # Input: list of stations
    # Called when the storage sends out an updated list of stations
    def update_stations(self, stations):
        if stations == "": return
        parsed = json.loads(stations)
        self.stations_cache = parsed


    # This method is called by the RpcServer waiting for requests.
    def on_message_received(self, request):
        if request == "": return
        request = json.loads(request)
        lat = float(request['Lat'])
        lon = float(request['Lon'])
        radius = float(request['RadiusKm'])

        stations_near_by = search(self.stations_cache, lat, lon, radius)

        departures_added_name = map_stations_to_departures(stations_near_by,
                                                           self.departures)

        return json.dumps(departures_added_name)


# Input: list of: local_stations,
# dict of: Uic -> departures
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
# def make_result(lat, lon, result):
#     res = {}
#     res['request'] = {'lat': lat, 'lon': lon}
#     res['result'] = result
#     return result


