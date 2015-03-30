# The health server

# Start consuming on the health queue.
import json

from DepartureTimes.communication.queues import health_queue_name
from DepartureTimes.communication.read_from_queue import RmqReader
from Health.data import T, M, TS, V
from Health.statistics import Statistics
from Stress.stress_send_query import baseline_average_search_time_ms


searchTimeLogFile = "./Health/data/health_%s.log"


statistics = None

def main():

    #exception_handler(start_health_service)
    start_health_service()

def start_health_service():
    global statistics

    mean_length = 4
    baseline = baseline_average_search_time_ms(mean_length) * 2
    statistics = Statistics(mean_length, baseline)

    reader = RmqReader(health_queue_name, health_message_handler)
    reader.start_consuming()


# Handles incoming health messages from RMQ
def health_message_handler(message):
    health = json.loads(message)
    health_type = health[T]
    health_measure = health[M]

    statistics.on_new_measure(health_measure)
    #write_to_log(health_type, health_measure)


def write_to_log(kind, measure):
    log_name = searchTimeLogFile % kind
    with open(log_name, "a+") as f:
        f.write("%s %s\n" % ("{0:.2f}".format(measure[TS]), measure[V]))
    f.close()


