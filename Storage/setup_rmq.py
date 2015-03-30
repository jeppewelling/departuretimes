import pika
from DepartureTimes.communication.interrupt_handler import block_signals
from DepartureTimes.communication.util import add_rpc_server_queue
from DepartureTimes.communication.queues \
    import storage_query_queue_name, storage_import_queue_name, departures_exchange, stations_exchange
from Storage.import_service import ImportServiceMessageHandler
from Storage.query_service import QueryServiceMessageHandler


class StorageRmq(object):
    def __init__(self, data_store):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        # Setup the query service
        add_rpc_server_queue(self.channel,
                             storage_query_queue_name,
                             QueryServiceMessageHandler(data_store).on_message_received)

        # The exchanges needed for publishing is setup
        self.channel.exchange_declare(exchange=departures_exchange, type='fanout')
        self.channel.exchange_declare(exchange=stations_exchange, type='fanout')


        # Setup the import service
        import_service = ImportServiceMessageHandler(data_store, self.stations_publish_message, self.departures_publish_message)
        self.add_read_only_queue(storage_import_queue_name,
                                 import_service.on_message_received)


        print "Storage ready"
        # Start consuming from the queues
        self.channel.start_consuming()

    def publish_message(self, exchange_name, message):
        self.channel.basic_publish(exchange=exchange_name,
                                   routing_key='',
                                   body=message)

    def departures_publish_message(self, message):
        self.publish_message(departures_exchange, message)

    def stations_publish_message(self, message):
        self.publish_message(stations_exchange, message)


    # Only reads from the queue
    def add_read_only_queue(self, queue_name, message_handler):
        self.channel.queue_declare(queue=queue_name, durable=True)
        print ' [*] Waiting for messages on Read queue: %r' % (queue_name)

        # The callback provided to rmq.
        def message_handler_callback(ch, method, properties, body):
            with block_signals():
                print "Received message on %r: " % (queue_name, )
                message_handler(body)
                ch.basic_ack(delivery_tag=method.delivery_tag)

        # Only dispatch one message to the worker at a time.
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(message_handler_callback,
                                   queue=queue_name)
