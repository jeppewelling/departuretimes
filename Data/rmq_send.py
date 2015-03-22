import json
from DepartureTimes.communication.send_to_queue import send
from DepartureTimes.communication.queues import storage_import_queue_name


def send_stations_to_storage(stations):
    send_to_storage(
        make_meta(
            stations,
            "stations"))
    print_message("stations")


def send_departures_to_storage(station, departures):
    send_to_storage(
        make_meta_for_departures(
            station,
            departures,
            "departures"))
    print " [x] Send departures from %r to storage on queue: %r "\
        % (station['Name'], storage_import_queue_name)


def send_cities_to_storage(cities):
    send_to_storage(
        make_meta(
            cities,
            "cities"))
    print_message("cities")


def make_meta(lst, data_type):
    meta = {'type': data_type, 'data': lst}
    return meta


def make_meta_for_departures(station, lst, data_type):
    meta = make_meta(lst, data_type)
    meta['FromStation'] = station
    return meta


def print_message(type_):
    print " [x] Send %r to storage on queue: %r "\
        % (type_, storage_import_queue_name)


def send_to_storage(imported_json):
    send(storage_import_queue_name, json.dumps(imported_json))
