# A system status monitor.

# monitors the search times and logs them to a local file used for
# plotting graphs.

import json

from DepartureTimes.communication.queues import health_queue_name
from Health.data import make_health_state, now_ms, make_measure
from Health.rmq import HealthSendRmqSetup


SearchTime = "SearchTime"
FetchStationsTime = "FetchStationsTime"
FetchDeparturesTime = "FetchDeparturesTime"



# Health point markers for the system
def health_check_search_time(measured_value):
    health_check(SearchTime, measured_value)


def health_check_fetch_stations(measured_value):
    health_check(FetchStationsTime, measured_value)


def health_check_fetch_departures(measured_value):
    health_check(FetchDeparturesTime, measured_value)

# Just use one single connection
rmq = HealthSendRmqSetup(health_queue_name)

buffer = []
cnt = 0
threshold = 100
def health_check(kind, measured_value):
    global cnt, threshold, buffer
    cnt += 1
    m = make_measure(measured_value)
    health = make_health_state(kind, m)
    buffer.append(json.dumps(health))

    if cnt % threshold == 0:
        s = now_ms()
        for m in buffer:
            rmq.send(m)
        buffer = []
        e = now_ms()
        d = e - s





