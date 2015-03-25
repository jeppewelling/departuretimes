#!/usr/bin/python
import json
import time

from DepartureTimes.communication.rpc_client import RpcClient
from DepartureTimes.communication.queues import query_queue_name
from Query.query_service import find_departures


if __name__ == "__main__":
    start = time.time()
    requests = 200
    i = 0
    while i < requests:
        find_departures(56.837871, 9.8927479, 10)
        i += 1
    print "i=%s" % i
    end = time.time()
    exec_time = end - start
    req_per_s = requests / exec_time

    print "Total requests: %s\nTotal time: %s seconds \nRequests per second: %s" % (requests, exec_time, req_per_s)
    
