import pika
from time import sleep
from interrupt_handler import block_signals

# A generic RPC server for RabbitMQ
# http://www.rabbitmq.com/tutorials/tutorial-six-python.html


# The response handler should be an object with a method:
#  on_message_received(string message)
class RpcServer(object):
    def __init__(self, queue_name, response_handler):
        self.consuming_started = False
        self.queue_name = queue_name
        self.connect()
        self.response_handler = response_handler

        try:
            self.connect()
        except Exception as ex:
            sleep_time = 10
            print "Received exception: %s, reconnecting in: %s seconds"\
                % (ex, sleep_time)
            sleep(sleep_time)
            self.connect()

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.on_request, queue=self.queue_name)

    def start_consuming(self):
        if self.consuming_started:
            return

        print " [x] Server: Awaiting RPC requests on queue: %r" \
            % self.queue_name

        self.consuming_started = True
        self.channel.start_consuming()

    def on_request(self, ch, method, props, body):
        with block_signals():
            response = self.response_handler.on_message_received(body)
            ch.basic_publish(exchange='',
                             routing_key=props.reply_to,
                             properties=pika.BasicProperties(
                                correlation_id=props.correlation_id),
                             body=response)
            ch.basic_ack(delivery_tag=method.delivery_tag)
