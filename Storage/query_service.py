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
import query

queue_name = 'storage_query'
data_store = None

def listen_for_queries(store):
    # fix later...
    global data_store
    data_store = store
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue=queue_name)
    print " [x] Awaiting RPC requests on queue: %r" % (queue_name)
    channel.start_consuming()


def on_request(ch, method, props, body):
    print "Received request, stand by for response."
    request = json.loads(body)
    response = json.dumps(handle_request(request))

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag = method.delivery_tag)


def make_meta(result, status):
    meta = {}
    meta['result'] = status
    meta['data'] = result
    return result


def handle_request(request):
    request_type = request['type']
    print "handling request: %r" % (request_type)

    print "The data_store for queries: %r " % (data_store)
    if request_type == "get_stations":
        return make_meta(data_store.get_stations(),
                         "Success")
        
    if request_type == "get_departures":
        stations = request['data']
        return make_meta(data_store.get_departures_from_stations(stations),
                         "Success")
        
    print "Request type unrecognized"
    return make_meta(request_type_not_found(), 
                     "Failed")


def request_type_not_found():
    res = {}
    res['message'] = 'Sorry, the request type '\
                     'was not recoginzed. Expected '\
                     'one of: get_stations, get_departures'
    return res

if __name__ == "__main__":
    from data_store import DataStore
    listen_for_queries(DataStore())
