import pika
import json
from DepartureTimes.communication.send_to_queue import send

queue_name = "storage_data_import"


def send_stations_to_storage(stations):
    send_to_storage(
        make_meta(
            stations, 
            "stations"))
    print_message("stations")


def send_departures_to_storage(station_id, departures):
    send_to_storage(
        make_meta_for_departures(
            station_id,
            departures, 
            "departures"))
    print_message("departures")


def send_cities_to_storage(cities):
    send_to_storage(
        make_meta(
            cities, 
            "cities"))
    print_message("cities")


def make_meta(lst, data_type):
    meta = {}
    meta['type'] = data_type
    meta['data'] = lst
    return meta


def make_meta_for_departures(station_id, lst, data_type):
    meta = make_meta(lst, data_type)
    meta['Uic'] = station_id
    return meta


def print_message(type_):
    print " [x] Send %r to storage on queue: %r " % (type_, queue_name)


def send_to_storage(imported_json):
    send(queue_name, json.dumps(imported_json))

