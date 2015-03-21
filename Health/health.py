# A system status monitor.

# monitors the search times and logs them to a local file used for
# plotting graphs.

import json
import time
from DepartureTimes.communication.read_from_queue import RmqReader
from DepartureTimes.communication.queues import health_queue_name
from DepartureTimes.communication.send_to_queue import send
from DepartureTimes.communication.interrupt_handler import exception_handler

# Health   ::= [<Type> <Measure>]
# Type     ::= SearchTime | ...
# Measure  ::= [<TimeStamp> <decimal>]

M = u'Measure'
T = u'Type'
TS = u'TimeStamp'
V = u'Value'

SearchTime = "SearchTime"
FetchStationsTime = "FetchStationsTime"
FetchDeparturesTime = "FetchDeparturesTime"

searchTimeLogFile = "./health_%s.log"


def main():
    exception_handler(start_health_service)


# Health point markers for the system
def health_check_search_time(measured_value):
    health_check(SearchTime, measured_value)


def health_check_fetch_stations(measured_value):
    health_check(FetchStationsTime, measured_value)


def health_check_fetch_departures(measured_value):
    health_check(FetchDeparturesTime, measured_value)


def health_check(kind, measured_value):
    health = make_health_state(kind, measured_value)
    send(health_queue_name, json.dumps(health))


# Start consuming on the health queue.
def start_health_service():
    reader = RmqReader(health_queue_name, health_message_handler)
    reader.start_consuming()


# Handles incomming health messages from RMQ
def health_message_handler(message):
    health = json.loads(message)
    health_type = health[T]
    health_measure = health[M]
    write_to_log(health_type, health_measure)


def write_to_log(kind, measure):
    log_name = searchTimeLogFile % kind
    with open(log_name, "a+") as f:
        f.write("%s %s\n" % (measure[TS], measure[V]))
    f.close()


def make_measure(ts, v):
    return {TS: ts, V: v}


def make_health_state(t, v):
    m = make_measure(int(time.time()), v)
    return {T: t, M: m}
