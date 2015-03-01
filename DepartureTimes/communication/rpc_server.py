import signal
import pika 
import json
import sys
from contextlib import contextmanager

# A generic RPC server for RabbitMQ


received_signal = False
processing_callback = False


# http://www.rabbitmq.com/tutorials/tutorial-six-python.html
class RpcServer(object):
    def __init__(self, queue_name, response_handler):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        self.queue_name = queue_name
        self.response_handler = response_handler

        self.channel = self.connection.channel()
        
        self.channel.queue_declare(queue=queue_name)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.on_request, queue=queue_name)

        print " [x] Server: Awaiting RPC requests on queue: %r" % queue_name
        self.channel.start_consuming()


    def on_request(self, ch, method, props, body):
        with block_signals:
            response = self.response_handler(body)
            ch.basic_publish(exchange='',
                             routing_key=props.reply_to,
                             properties=pika.BasicProperties(
                                 correlation_id = props.correlation_id),
                             body=response)
            ch.basic_ack(delivery_tag = method.delivery_tag)
        



# Handle signals from the outside environment i.e. stop start.
def signal_handler(signal, frame):
    global received_signal
    print "signal received"
    received_signal = True
    if not processing_callback:
         sys.exit()

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

@contextmanager
def block_signals():
    global processing_callback
    processing_callback = True
    try:
        yield
    finally:
        processing_callback = False
        if received_signal:
            sys.exit()

