import pika
import json

queue_name = "train_departures"

def make_meta(lst, data_type):
    meta = {}
    meta['type'] = data_type
    meta['data'] = lst
    return meta


def send_station_list_to_storage(stations):
    send_to_storage(
        make_meta(
            stations, 
            "stations"))

def send_departures_to_storage(departures):
    send_to_storage(
        make_meta(
            departures, 
            "departures"))



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



