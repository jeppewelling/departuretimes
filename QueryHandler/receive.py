#!/usr/bin/env python
import pika
import json

queue_name = 'departureinfo_query'

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()

channel.queue_declare(queue=queue_name)

def look_up(request):
    lat = request['lat']
    lon = request['lon']

    print " [.] request: %s %s"  % (lat, lon)
    res = {}
    res['request'] = { 'lat' : lat, 'lon' : lon}
    res['result'] = 'Service is not available yet...'
    return json.dumps(res)

def on_request(ch, method, props, body):
    request = json.loads(body)

    response = look_up(request)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue=queue_name)

print " [x] Awaiting RPC requests"
channel.start_consuming()

