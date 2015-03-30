import json
from communication.rpc_client import RpcClient
from communication.health_client_rmq import HealthClient
from communication.queues import query_queue_name


# Sends a query to the Query sevice
# returns an answer as JSON represented as a dict

def find_departures(lat, lon, radius):
    health = HealthClient()
    rpc = RpcClient(query_queue_name)
    #health.begin_search_time_measure()
    res = json.loads(rpc.call(encode_message(lat, lon, radius)))
    #health.end_search_time_measure()
    rpc.close()
    health.close()
    return res


def encode_message(lat, lon, radius):
    req = {'Lat': lat, 'Lon': lon, 'RadiusKm': radius}
    return json.dumps(req)

