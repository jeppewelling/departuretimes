import pika
import uuid
import json

queue_name = 'departureinfo_query'

def send_to_query_handler(lat, lon):
    fibonacci_rpc = DepartureTimeRpcClient()

    print " [x] Requesting %s %s" % (lat, lon)
    response = fibonacci_rpc.call(lat, lon)

    print " [.] Got %r" % (response,)
    return response

# Using RMQ RPC:
# http://www.rabbitmq.com/tutorials/tutorial-six-python.html
class DepartureTimeRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))

        self.channel = self.connection.channel()
        
        # Define a callback queue (not named)
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, lat, lon):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key=queue_name,
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=encode_message(lat, lon))
        while self.response is None:
            self.connection.process_data_events()
        return self.response


def encode_message(lat, lon):
    req = {}
    req['lat'] = lat
    req['lon'] = lon
    return json.dumps(req)





