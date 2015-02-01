# A service for querying the storage
# 
# The storage offers the following queries:
# - get_stations: 
#   Get list of stations with geolocations
#
# - get_departures_from_stations: 
#   Given a list of stations, return a list of 
#   departures from those stations
import pika
import json
from DepartureTimes.communication.rpc_server import RpcServer

queue_name = 'storage_query'
store = None

def listen_for_queries(store_):
    # fix later...
    global store
    store = store_
    rpc = RpcServer(queue_name, handle_request)


def handle_request(request):
    request = json.loads(request)
    request_type = request['type']
    print "handling request: %r" % (request_type)

    if request_type == "get_stations":
        return json.dumps(make_meta(store.get_stations(),
                                    "Success"))
        
    if request_type == "get_departures":
        stations = request['data']
        return json.dumps(make_meta(store.get_departures_from_stations(stations),
                                    "Success"))
        
    print "Request type unrecognized"
    return json.dumps(make_meta(request_type_not_found(), 
                                "Failed"))


def make_meta(result, status):
    meta = {}
    meta['result'] = status
    meta['data'] = result
    return result


def request_type_not_found():
    res = {}
    res['message'] = 'Sorry, the request type '\
                     'was not recoginzed. Expected '\
                     'one of: get_stations, get_departures'
    return res

if __name__ == "__main__":
    from data_store import DataStore
    listen_for_queries(DataStore())
