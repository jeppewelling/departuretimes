#!/usr/bin/env python
import pika
import json
from search import get_stations_near
from DepartureTimes.communication.rpc_server import RpcServer
from read_from_storage import storage_query_get_stations

queue_name = 'departureinfo_query'

def make_result(lat, lon, result):
    res = {}
    res['request'] = { 'lat' : lat, 'lon' : lon}
    res['result'] = result
    return result


def look_up(request):
    request = json.loads(request)
    lat = float(request['lat'])
    lon = float(request['lon'])
    stations = storage_query_get_stations()

    # Currently returns the stations near by, but should also 
    # return departures for each stataion
    stations_near_by =  get_stations_near(lat, lon, 20, stations)
    print " [.] request: %s %s %s"  % (lat, lon, stations_near_by)
    return json.dumps(make_result(lat, lon, stations_near_by))


if __name__ == "__main__":
    RpcServer(queue_name, look_up)
