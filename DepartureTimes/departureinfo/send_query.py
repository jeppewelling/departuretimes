import json
from communication.rpc_client import RpcClient


queue_name = 'departureinfo_query'

# Sends a query to the QueryHandler
def send_to_query_handler(lat, lon):
    rpc = RpcClient(queue_name)
    return rpc.call(encode_message(lat, lon))


def encode_message(lat, lon):
    req = {}
    req['lat'] = lat
    req['lon'] = lon
    return json.dumps(req)


if __name__ == "__main__":
    print send_to_query_handler(56.1500, 10.2167)

