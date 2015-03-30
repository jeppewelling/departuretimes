import signal

import pika

from DepartureTimes.communication.util import add_rpc_server_queue
from Storage.setup_rmq import StorageRmq
from data_store import DataStore
from Storage.query_service import QueryServiceMessageHandler
from Storage.import_service import ImportServiceMessageHandler
from DepartureTimes.communication.interrupt_handler \
    import signal_handler, block_signals
from DepartureTimes.communication.queues \
    import storage_query_queue_name, storage_import_queue_name
from DepartureTimes.communication.queues import departures_exchange, stations_exchange


def main():
    #exception_handler(setup)
    setup()


def setup():
    setup_termination_handling()
    setup_queues()


# Setup handling for termination
def setup_termination_handling():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()


# Setup the RMQ queues for data import and data queries
def setup_queues():
    data_store = DataStore()
    rmq = StorageRmq(data_store)

#     # Setup the query service
#     add_rpc_server_queue(channel,
#                   storage_query_queue_name,
#                   QueryServiceMessageHandler(data_store).on_message_received)
#
#     # The exchanges needed for publishing is setup
#     declare_exchanges_for_publishing(channel, [departures_exchange, stations_exchange])
#
#
#     # Setup the import service
#     import_service = ImportServiceMessageHandler(data_store, stations_publish_message, departures_publish_message)
#     add_read_only_queue(channel,
#                          storage_import_queue_name,
#                          import_service.on_message_received)
#
#
#     print "Storage ready"
#     # Start consuming from the queues
#     channel.start_consuming()
#
#
# def departures_publish_message(message):
#     publish_message(departures_exchange, message)
#
# def stations_publish_message(message):
#     publish_message(stations_exchange, message)
#
# def publish_message(exchange_name, message):
#     channel.basic_publish(exchange=exchange_name,
#                           routing_key='',
#                           body=message)
#
#
# def declare_exchanges_for_publishing(channel, exchange_names):
#     for exchange_name in exchange_names:
#         channel.exchange_declare(exchange=exchange_name,
#                                  type='fanout')
#
#
# # Only reads from the queue
# def add_read_only_queue(channel, queue_name, message_handler):
#     channel.queue_declare(queue=queue_name, durable=True)
#     print ' [*] Waiting for messages on Read queue: %r' % (queue_name)
#
#     # The callback provided to rmq.
#     def message_handler_callback(ch, method, properties, body):
#         with block_signals():
#             print "Received message on %r: " % (queue_name, )
#             message_handler(body)
#             ch.basic_ack(delivery_tag=method.delivery_tag)
#
#     # Only dispatch one message to the worker at a time.
#     channel.basic_qos(prefetch_count=1)
#     channel.basic_consume(message_handler_callback,
#                           queue=queue_name)


