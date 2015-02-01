import pika
import json

queue_name = "storage_data_import"

def make_meta(lst, data_type):
    meta = {}
    meta['type'] = data_type
    meta['data'] = lst
    return meta

def make_meta_for_departures(station_id, lst, data_type):
    meta = make_meta(lst, data_type)
    meta['Uic'] = station_id
    return meta


def send_stations_to_storage(stations):
    send_to_storage(
        make_meta(
            stations, 
            "stations"))

def send_departures_to_storage(station_id, departures):
    send_to_storage(
        make_meta_for_departures(
            station_id,
            departures, 
            "departures"))

def send_cities_to_storage(cities):
    send_to_storage(
        make_meta(
            cities, 
            "cities"))



# Thanks to:
# http://www.rabbitmq.com/tutorials/tutorial-one-python.html
def send_to_storage(imported_json):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue=queue_name)
    
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=json.dumps(imported_json))
    print " [x] Send DSB data to storage"
    connection.close()



