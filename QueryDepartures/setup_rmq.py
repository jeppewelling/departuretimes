# The query service is capable of:
# - Requesting the storage
# - Listening to updates from the storage
# - Listening to query requests from users

import json
import traceback
import pika
from DepartureTimes.communication.interrupt_handler import rpc_exception_handler

from DepartureTimes.communication.rpc_client import RpcChannelClient
from DepartureTimes.communication.util import add_rpc_server_queue
from DepartureTimes.communication.queues import storage_query_queue_name, query_queue_name
from DepartureTimes.communication.queues import departures_exchange, stations_exchange


class RmqSetup(object):
    # Input: a list of {ExchangeName: e, MessageHandler: m}
    def __init__(self, query_service):
        self.query_service = query_service
        self.connect()


    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        self.channel = self.connection.channel()

        # enable the query to make RPCs on the storage
        self.rpc_storage = RpcChannelClient(self.connection, self.channel, storage_query_queue_name)

        # A helper for subscribing to an exchange
        def subscribe_to_exchange(exchange_name, message_handler):
            def callback(ch, method, properties, body):
                message_handler(body)

            self.channel.exchange_declare(exchange=exchange_name,
                                          type='fanout')
            result = self.channel.queue_declare(exclusive=True)
            queue_name = result.method.queue
            self.channel.queue_bind(exchange=exchange_name,
                                    queue=queue_name)

            self.channel.basic_consume(callback,
                                       queue=queue_name,
                                       no_ack=True)


        subscribe_to_exchange(departures_exchange, self.query_service.update_departures)
        subscribe_to_exchange(stations_exchange, self.query_service.update_stations)

        # Setup the rpc service for finding stations
        add_rpc_server_queue(self.channel, query_queue_name, self.query_service.on_message_received)



    def fetch_stations_from_storage(self):
        q = {'type': "get_stations"}
        self.query_service.update_stations(self.rpc_storage.call(json.dumps(q)))



    def fetch_all_departures_from_storage(self):
        q = {'type': "get_all_departures", 'data': []}
        # If the storage service is offline, we get a time out and nothing is returned.
        # Once the storage service is online, it will send the data to us.
        self.query_service.update_departures(self.rpc_storage.call(json.dumps(q)))


    def start_listening(self):
        with rpc_exception_handler():
            self.channel.start_consuming()

