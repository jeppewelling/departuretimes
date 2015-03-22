import pika

# A class for subscribing to an exchange
# Thanks to
# https://www.rabbitmq.com/tutorials/tutorial-three-python.html

class Subscribe(object):
    # Input: a list of {ExchangeName: e, MessageHandler: m}
    def __init__(self, exchange_names_and_message_handlers):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        self.channel = self.connection.channel()

        def add_to_exchange(exchange_name, message_handler):
            def callback(ch, method, properties, body):
                message_handler(body)

            self.channel.exchange_declare(exchange=exchange_name,
                                          type='fanout')
            result = self.channel.queue_declare(exclusive=True)
            queue_name = result.method.queue
            self.channel.queue_bind(exchange=self.exchange_name,
                                    queue=queue_name)
            self.channel.basic_consume(callback,
                                       queue=queue_name,
                                       no_ack=True)

        for e in exchange_names_and_message_handlers:
            exchange_name = e['ExchangeName']
            message_handler = e['MessageHandler']
            add_to_exchange(exchange_name, message_handler)



    def subscribe(self):
        print ' [Subscribe] Waiting for messages...'
        self.channel.start_consuming()