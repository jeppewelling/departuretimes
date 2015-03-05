import pika
import signal
from data_store import DataStore
from query_service import QueryServiceMessageHandler
from import_service import ImportServiceMessageHandler
from DepartureTimes.communication.interrupt_handler \
    import signal_handler, block_signals, exception_handler
from DepartureTimes.communication.queues \
    import storage_query_queue_name, storage_import_queue_name


def main():
    exception_handler(setup)


def setup():
    setup_termination_handling()
    setup_queues()


# Setup handling for termination
def setup_termination_handling():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


# Setup the RMQ queues for data import and data queries
def setup_queues():
    data_store = DataStore()

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    # Setup the query service
    add_rpc_queue(channel,
                  storage_query_queue_name,
                  QueryServiceMessageHandler(data_store))

    # Setup the import service
    add_read_only_queue(channel,
                        storage_import_queue_name,
                        ImportServiceMessageHandler(data_store))

    # Start consuming from the queues
    channel.start_consuming()


# Only reads from the queue
def add_read_only_queue(channel, queue_name, message_handler):
    channel.queue_declare(queue=queue_name, durable=True)
    print ' [*] Waiting for messages on Read queue: %r' % (queue_name)

    # The callback proviced to rmq.
    def message_handler_callback(ch, method, properties, body):
        with block_signals():
            print "Received message on %r: " % (queue_name, )
            message_handler.on_message_received(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)

    # Only dispatch one message to the worker at a time.
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(message_handler_callback,
                          queue=queue_name)


# Reads from the queue and immediately sends back an answer to the sender.
def add_rpc_queue(channel, queue_name, message_handler):
    channel.queue_declare(queue=queue_name)

    # The message handler calls back to the sender.
    def message_handler_callback(ch, method, properties, body):
        with block_signals():
            print "Received message on %r: %r" % (queue_name, body)
            response = message_handler.on_message_received(body)
            ch.basic_publish(exchange='',
                             routing_key=properties.reply_to,
                             properties=pika.BasicProperties(
                                 correlation_id=properties.correlation_id),
                             body=response)
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(message_handler_callback,
                          queue=queue_name)
    print " [x] Waiting for messages on RPC queue: %r" \
        % queue_name

