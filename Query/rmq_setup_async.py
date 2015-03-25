import json
import traceback
import logging
import pika
from DepartureTimes.communication.interrupt_handler import rpc_exception_handler, block_signals
from DepartureTimes.communication.rpc_client import RpcChannelClient
from DepartureTimes.communication.util import add_rpc_server_queue
from DepartureTimes.communication.queues import storage_query_queue_name, query_queue_name
from DepartureTimes.communication.queues import departures_exchange, stations_exchange

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')

LOGGER = logging.getLogger(__name__)


class RmqSetup(object):

    # Input: a list of {ExchangeName: e, MessageHandler: m}
    def __init__(self, query_service):
        self.query_service = query_service


    def connect(self):
        return pika.SelectConnection(pika.ConnectionParameters(host='localhost'),
                                     self.on_connection_open,
                                     stop_ioloop_on_close=False)

    def run(self):
        self.connection = self.connect()
        self.connection.ioloop.start()

    def on_connection_open(self, connection):
        self.connection.add_on_close_callback(self.on_connection_closed)
        self.connection.channel(on_open_callback=self.on_channel_open)



    def on_channel_open(self, channel):
        LOGGER.info('Channel opened')
        self.channel = channel
        self.add_on_channel_close_callback()

        # enable the query to make RPCs on the storage
        self.rpc_storage = RpcChannelClient(self.connection, self.channel, storage_query_queue_name)

        # Setting up the exchanges for subscribing to departures and stations
        self.setup_exchange(departures_exchange, self.query_service.update_departures)
        self.setup_exchange(stations_exchange, self.query_service.update_stations)

        # Setup the rpc service for finding stations
        self.add_rpc_server_queue(query_queue_name, self.query_service.on_message_received)



    def add_rpc_server_queue(self, queue_name, message_handler):
        # The message handler calls back to the sender.
        def message_handler_callback(ch, method, properties, body):
            with block_signals():
                response = message_handler(body)
                ch.basic_publish(exchange='',
                                 routing_key=properties.reply_to,
                                 properties=pika.BasicProperties(
                                     correlation_id=properties.correlation_id),
                                 body=response)
                ch.basic_ack(delivery_tag=method.delivery_tag)

        def on_queue_declareok(method):
            with rpc_exception_handler():
                self.channel.basic_consume(message_handler_callback,
                                           queue=queue_name)

        self.channel.queue_declare(callback=on_queue_declareok,
                                   queue=queue_name)






    def add_on_channel_close_callback(self):
        LOGGER.info('Adding channel close callback')
        self.channel.add_on_close_callback(self.on_channel_closed)



    def on_connection_closed(self, connection, reply_code, reply_text):
        self.channel = None
        if self.closing:
            self.connection.ioloop.stop()
        else:
            LOGGER.warning('Connection closed, reopening in 5 seconds: (%s) %s',
                           reply_code, reply_text)
            self._connection.add_timeout(5, self.reconnect)




    # A helper for subscribing to an exchange
    def setup_exchange(self, exchange_name, message_handler):

        self.channel.exchange_declare(callback=lambda frame: self.on_exchange_declareok(frame, exchange_name, message_handler),
                                      exchange=exchange_name,
                                      type='fanout')

    def on_exchange_declareok(self, frame, exchange_name, message_handler):
        print "Declared exchange: %s" % exchange_name

        def on_queue_declareok(method_frame):
            queue_name = method_frame.method.queue
            print "Queue declared: %s, exchange: %s " % (queue_name, exchange_name)
            def callback(ch, method, properties, body):
                print "update stations: %s on queue: %s" % (body, queue_name)
                message_handler(body)

            def on_queue_bound(frame):
                print "queue bound: %s" % queue_name
                self.channel.basic_consume(callback,
                                           queue=queue_name,
                                           no_ack=True)


            self.channel.queue_bind(callback=on_queue_bound,
                                    exchange=exchange_name,
                                    queue=queue_name)


        self.channel.queue_declare(callback=on_queue_declareok, exclusive=True)






    def on_channel_closed(self, channel, reply_code, reply_text):
        LOGGER.warning('Channel %i was closed: (%s) %s',
                       channel, reply_code, reply_text)
        self._connection.close()



    def fetch_stations_from_storage(self):
        q = {'type': "get_stations"}
        stations = self.rpc_storage.call(json.dumps(q))
        self.query_service.update_stations(stations)


    def fetch_all_departures_from_storage(self):
        q = {'type': "get_all_departures", 'data': []}
        self.query_service.update_departures(self.rpc_storage.call(json.dumps(q)))




    def start_listening(self):
        self.add_on_cancel_callback()
        self.channel.start_consuming()
        #self._channel.basic_consume(self.on_message, self.QUEUE)


    def add_on_cancel_callback(self):
        LOGGER.info('Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)


        # def start_listening(self):
        #     #with rpc_exception_handler():
        #     try:
        #         print ' [Query] Waiting for messages...'
        #         self.channel.start_consuming()
        #
        #     # On exception lets just try once to reconnect else let it crash
        #     # TODO send health information about this crash
        #     except Exception as ex:
        #         print "RMQ error, trying to reconnect..."
        #         traceback.print_exc()
        #         self.connect()
        #         self.channel.start_consuming()




# A rpc client for an existing channel
class RpcChannelClient(object):
    def __init__(self, connection, channel, queue_name):
        self.connection = connection
        self.channel = channel
        self.queue_name = queue_name
        # Define a callback queue (not named)
        print "Hest: %s" % channel
        result = channel.queue_declare(callback=self.on_queue_declareok, exclusive=True)

    def on_queue_declareok(self, method_frame):
        self.callback_queue = method_frame.method.queue
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
            try:
                self.connection.process_data_events()
            # If we lose the connection to the end point just skip
            except Exception:
                return ""
        return self.response
__author__ = 'jwh'
