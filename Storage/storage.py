import signal

import pika

from DepartureTimes.communication.util import add_rpc_server_queue
from Storage.setup_rmq import StorageRmq
from data_store import DataStore
from Storage.query_service import QueryServiceMessageHandler
from Storage.import_service import ImportServiceMessageHandler
from DepartureTimes.communication.interrupt_handler \
    import signal_handler, block_signals, exception_handler
from DepartureTimes.communication.queues \
    import storage_query_queue_name, storage_import_queue_name
from DepartureTimes.communication.queues import departures_exchange, stations_exchange


def main():
    exception_handler(setup)
    #setup()


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
    StorageRmq(data_store)

