#!/usr/bin/env python
import pika
import json
from search import get_stations_near
from DepartureTimes.communication.rpc_server import RpcServer
from read_from_storage import storage_query_get_stations, storage_query_get_departures

queue_name = 'departureinfo_query'


# Wraps the result to be returned to the client
def make_result(lat, lon, result):
    res = {}
    res['request'] = { 'lat' : lat, 'lon' : lon}
    res['result'] = result
    return result


# Handles the request by the web client
def handle_web_client_request(request):
    request = json.loads(request)
    lat = float(request['Lat'])
    lon = float(request['Lon'])
    radius = float(request['RadiusKm'])

    # Get the entire list of stations to search for the losest one It
    # is a bit naive to just get the entire list, but the idea is to
    # seperate responsibility. The store only stores data and the
    # QueryHandler does the calculations.
    stations = storage_query_get_stations()

    # Currently returns the stations near by, but should also 
    # return departures for each stataion
    stations_near_by =  get_stations_near(lat, lon, radius, stations)

    # Get departures for local stations.  Stations with no departures
    # are weeded out, thus there is no guarantee that there is a
    # mapping for each local station.
    departures = storage_query_get_departures(stations_near_by)
    departures_added_name = add_from_name_to_departures(stations_near_by, 
                                                        departures)

    return json.dumps(make_result(lat, lon, departures_added_name))


def add_from_name_to_departures(local_stations, departures):
    out = []
    for station in local_stations:
        uic = station['Uic']
        # There might not be a mapping for each local station to a
        # list of departures
        if uic in departures:
            departures_from_station = departures[uic]
            out.append(append_from_station_name(station, departures_from_station, uic))

    return out

def append_from_station_name(station, departures_from_station, uic):
    return {"Uic": uic,
            "DepartureName" : station['Name'],
            "Departures" : departures_from_station }


if __name__ == "__main__":
    RpcServer(queue_name, handle_web_client_request)
