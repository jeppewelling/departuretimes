# A generic RPC client


# Using RMQ RPC:
# http://www.rabbitmq.com/tutorials/tutorial-six-python.html

import sys
import uuid
import pika



class RpcClient(object):
    def __init__(self, queue_name):
        print "new rpc client"
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
                                         reply_to=self.callback_queue,
                                         correlation_id=self.corr_id),
                                   body=message)
        while self.response is None:
            #sys.stdout.write('+')
            self.connection.process_data_events()
        return self.response


    def close(self):
        self.connection.close()



# A rpc client for an existing channel
class RpcChannelClient(object):
    def __init__(self, connection, channel, queue_name):
        self.connection = connection
        self.channel = channel
        self.queue_name = queue_name
        # Define a callback queue (not named)

        result = channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, message):
        #ensure_data_events_are_processed(self.channel)
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   properties=pika.BasicProperties(
                                         reply_to=self.callback_queue,
                                         correlation_id=self.corr_id),
                                   body=message)
        print "RPC Begin"
        while self.response is None:
            try:
                sys.stdout.write('.')
                self.connection.process_data_events()
            # If we lose the connection to the end point just skip
            except Exception as ex:
                return "Exception: %s" % ex
        print "RPC Finish"
        return self.response
