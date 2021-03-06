#!/usr/bin/python
import json
from DepartureTimes.communication.rpc_client import RpcClient
from DepartureTimes.communication.queues import query_queue_name


# Sends a query to the QueryHandler
def send_to_query_handler(lat, lon, radius):
    rpc = RpcClient(query_queue_name)
    return rpc.call(encode_message(lat, lon, radius))


def encode_message(lat, lon, radius):
    req = {}
    req['Lat'] = lat
    req['Lon'] = lon
    req['RadiusKm'] = radius
    return json.dumps(req)


if __name__ == "__main__":
    print send_to_query_handler(56.1500, 10.2167, 100)
