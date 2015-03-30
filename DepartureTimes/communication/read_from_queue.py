from time import sleep
import pika

# A generic queue reader


class RmqReader(object):
    def __init__(self, queue_name, message_handler):
        self.consuming_started = False
        self.queue_name = queue_name
        self.message_handler = message_handler
        # try:
        self.connect()
        # except Exception as ex:
        #     sleep_time = 10
        #     print "Received exception: %s, reconnecting in: %s seconds"\
        #         % (ex, sleep_time)
        #     sleep(sleep_time)
        #     self.connect()

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.channel.basic_consume(self.on_request,
                                   queue=self.queue_name,
                                   no_ack=True)

    def start_consuming(self):
        if self.consuming_started:
            return
        print ' [*] Waiting for messages on queue: %r' % (self.queue_name)
        self.consuming_started = True
        self.channel.start_consuming()

    def on_request(self, ch, method, properties, body):
        self.message_handler(body)
