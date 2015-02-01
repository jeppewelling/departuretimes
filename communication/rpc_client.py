import pika 
import uuid
import json


# Using RMQ RPC:
# http://www.rabbitmq.com/tutorials/tutorial-six-python.html
class RpcClient(object):
    def __init__(self, queue_name):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))

        self.queue_name = queue_name
        self.channel = self.connection.channel()
        
        # Define a callback queue (not named)
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=message)
        while self.response is None:
            self.connection.process_data_events()
        return self.response
