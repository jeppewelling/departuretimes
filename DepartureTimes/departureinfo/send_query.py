import json
from communication.rpc_client import RpcClient
from communication.queues import query_queue_name


# Sends a query to the QueryHandler
# returns an answer as JSON represented as a dict
def send_to_query_handler(lat, lon, radius):
    rpc = RpcClient(query_queue_name)
    return json.loads(rpc.call(encode_message(lat, lon, radius)))


def encode_message(lat, lon, radius):
    req = {}
    req['Lat'] = lat
    req['Lon'] = lon
    req['RadiusKm'] = radius
    return json.dumps(req)


if __name__ == "__main__":
    print send_to_query_handler(56.1500, 10.2167, 100)
    
