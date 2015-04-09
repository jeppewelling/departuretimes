# The health server

# Start consuming on the health queue.
import json
from DepartureTimes.communication.interrupt_handler import exception_handler

from DepartureTimes.communication.queues import health_queue_name
from DepartureTimes.communication.read_from_queue import RmqReader
from Health.data import T, M, TS, V
from Health.statistics import Statistics
from config import HEALTH_LOG


searchTimeLogFile = HEALTH_LOG


statistics = None

def main():
    exception_handler(start_health_service)
    #start_health_service()

def start_health_service():
    global statistics

    # Set low for demonstration purposes
    mean_length = 4

    # The expected time for a search request to enter the query queue in the apache application
    # and until it has been processed and returned (in ms):
    baseline = 50
    statistics = Statistics(mean_length, baseline)

    reader = RmqReader(health_queue_name, health_message_handler)
    reader.start_consuming()


# Handles incoming health messages from RMQ
def health_message_handler(message):
    health = json.loads(message)
    health_type = health[T]
    health_measure = health[M]

    statistics.on_new_measure(health_measure)
    write_to_log(health_type, health_measure)


def write_to_log(kind, measure):
    log_name = searchTimeLogFile % kind
    with open(log_name, "a+") as f:
        f.write("%s %s\n" % ("{0:.2f}".format(measure[TS]), measure[V]))
    f.close()


