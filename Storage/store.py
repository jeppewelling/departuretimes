import pika
import json

queue_name = "train_departures"

stations_index = {}
cities_index = {}


def remove_end_word(string, endword):
    if string.endswith(endword):
        return string[:-len(endword)]
    return string
    

def strip_from_city_name(city_name):
    city_name = remove_end_word(city_name, " Central")
    city_name = remove_end_word(city_name, "C")
    return city_name.strip()

def index_stations(stations):
    stations_index.clear()
    for s in stations:
        stations_index[s['Uic']] = s


def index_cities(cities):
    cities_index.clear()
    for c in cities:
        name = strip_from_city_name(c['Name'])
        cities_index[name] = c

    


# Thanks to:
# http://www.rabbitmq.com/tutorials/tutorial-one-python.html
def receive_imports():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue=queue_name)
    
    print ' [*] Waiting for messages. To exit press CTRL+C'
    
    def callback(ch, method, properties, body):
        raw = json.loads(body)
        data_type = raw['type']
        data = raw['data']
        count = len(data)

        if data_type == "stations":
            index_stations(data)

        if data_type == "cities":
            index_cities(data)

        if data_type == "departures":
            departures_from = raw['Uic']
            city = strip_from_city_name(stations_index[departures_from]['Name'])
            loc = cities_index[city]
            lat = loc['lat']
            lon = loc['lon']
            print " [x] Received %r %r %r at location: %r:%r" % (data_type, 
                                                                 count, 
                                                                 city, 
                                                                 lat,
                                                                 lon)
        else:
            print " [x] Received %r %r" % (data_type, count)
        
    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)
        
    channel.start_consuming()

if __name__ == "__main__":
    receive_imports()
