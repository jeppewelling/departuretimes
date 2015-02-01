import pika
import json
from DepartureTimes.communication.read_from_queue import read

queue_name = "storage_data_import"
store = None


def message_handler(body):
    raw = json.loads(body)
    data_type = raw['type']
    data = raw['data']
    count = len(data)
    print " [x] Received %r %r" % (data_type, count)
    
    if data_type == u'stations':
        print "Storing stations"
        store.index_stations(data)
        
    if data_type == u'cities':
        print "Storing cities"
        store.index_cities(data)
            

    if data_type == u'departures':
        print "Storing departures"

        from_station = raw['FromStation']
        from_station_id = from_station['Uic']
        from_station_name = from_station['Name']
        store.add_to_departures_index(from_station_id, data)

        print "from_station: %r" % from_station

        loc = store.get_location_from_station_name(from_station_name)
        lat = -1
        lon = -1
        if loc != None:
            lat = loc['Lat']
            lon = loc['Lon']

        print " [x] Received %r %r %r at location: %r:%r" % (data_type, 
                                                             count, 
                                                             from_station_name, 
                                                             lat,
                                                             lon)
    

def listen_for_imports(store_):
    global store
    store = store_
    read(queue_name, message_handler)

if __name__ == "__main__":
    from data_store import DataStore
    listen_for_imports(DataStore())
    
