#!/usr/bin/python
import json

from DepartureTimes.communication.rpc_client import RpcClient
from DepartureTimes.communication.queues import query_queue_name


# Sends a query to the QueryHandler
# returns an answer as JSON represented as a dict
def send_to_query_handler(lat, lon, radius):
    rpc = RpcClient(query_queue_name)
    print "[Test send] Sending query..."
    return json.loads(rpc.call(encode_message(lat, lon, radius)))


def encode_message(lat, lon, radius):
    req = {'Lat': lat, 'Lon': lon, 'RadiusKm': radius}
    return json.dumps(req)


if __name__ == "__main__":
    #print send_to_query_handler(56.837871, 9.8927479, 10)
    print send_to_query_handler(56.5651232, 9.0309083, 10)


