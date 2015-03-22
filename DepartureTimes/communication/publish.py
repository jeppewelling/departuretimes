import pika

# A class for publishing to an exchange
# Thanks to
# https://www.rabbitmq.com/tutorials/tutorial-three-python.html

class Publish(object):
    def __init__(self, exchange_name):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=exchange_name,
                             type='fanout')


    def publish(self, message):
        self.channel.basic_publish(exchange='logs',
                              routing_key='',
                              body=message)

    def close(self):
        self.connection.close()
