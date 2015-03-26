#!/usr/bin/python
import time
from Health.data import now_ms

from Query.query_service import find_departures, find_departures_no_health_logging


def baseline_average_search_time_ms(iterations):
    start = now_ms()
    i = 0
    while i < iterations:
        find_departures_no_health_logging(56.837871, 9.8927479, 10)
        i += 1
    end = now_ms()
    exec_time = end - start
    average = exec_time / iterations
    return average


if __name__ == "__main__":
    start = now_ms()
    # Should take about 30 seconds
    requests = 7000
    i = 0
    while i < requests:
        find_departures(56.837871, 9.8927479, 10)
        i += 1
    print "i=%s" % i
    end = now_ms()
    exec_time = end - start
    req_per_s = (requests / (exec_time / 1000))
    average = exec_time / requests

    print "Total requests: %s\nTotal time: %s seconds \nRequests per second: %s\nAverage: %s ms per request incl sending to health" % (requests, exec_time / 1000, req_per_s, average)
    
