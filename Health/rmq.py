import pika

# The RMQ setup for sending messages to the health service

class HealthSendRmqSetup(object):
    def __init__(self, queue_name):
        self.connection = None
        self.channel = None
        self.queue_name = queue_name
        self.connect()

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)


    def send(self, data):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=data,
                                   properties=pika.BasicProperties(
                                       delivery_mode=1,  # make message non-persistent
                                   ))

    def close(self):
        self.connection.close()
