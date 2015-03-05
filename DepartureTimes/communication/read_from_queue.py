import pika

# A generic queue reader


class RmqReader(object):
    def __init__(self, queue_name, message_handler):
        self.consuming_started = False
        self.queue_name = queue_name
        self.message_handler = message_handler

    def read(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)
        
        def callback(ch, method, properties, body):
            self.message_handler(body)

        channel.basic_consume(callback,
                              queue=self.queue_name,
                              no_ack=True)

    def start_consuming(self):
        if self.consuming_started:
            return

        print ' [*] Waiting for messages on queue: %r' % (self.queue_name)

        self.channel.start_consuming()
        self.consuming_started = True

