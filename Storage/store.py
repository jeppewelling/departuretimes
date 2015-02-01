import pika
import json

queue_name = "storage_data_import"

store = None

# Thanks to:
# http://www.rabbitmq.com/tutorials/tutorial-one-python.html
def listen_for_imports(store_):
    global store
    store = store_
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue=queue_name)
    
    print ' [*] Waiting for messages on queue: %r' % (queue_name)
    
    def callback(ch, method, properties, body):
        raw = json.loads(body)
        data_type = raw['type']
        data = raw['data']
        count = len(data)
        print " [x] Received %r %r" % (data_type, count)
        print "The data_store for imports: %r " % (store)

        if data_type == u'stations':
            print "Storing stations"
            store.index_stations(data)
            store.get_stations()

        if data_type == u'cities':
            print "Storing cities"
            store.index_cities(data)


        if data_type == u'departures':
            print "Storing departures"

            departures_from = raw['Uic']
            store.add_to_departures_index(departures_from, data)

            # temp printing
            import data_store
            city = data_store.strip_from_city_name(store.stations_index[departures_from]['Name'])
            loc = store.cities_index[city]
            lat = loc['Lat']
            lon = loc['Lon']
            print " [x] Received %r %r %r at location: %r:%r" % (data_type, 
                                                                 count, 
                                                                 city, 
                                                                 lat,
                                                                 lon)
        
    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)
        
    channel.start_consuming()

if __name__ == "__main__":
    from data_store import DataStore
    listen_for_imports(DataStore())
