import json
from communication.rpc_client import RpcClient


queue_name = 'departureinfo_query'

# Sends a query to the QueryHandler
def send_to_query_handler(lat, lon, radius):
    rpc = RpcClient(queue_name)
    return rpc.call(encode_message(lat, lon, radius))


def encode_message(lat, lon, radius):
    req = {}
    req['Lat'] = lat
    req['Lon'] = lon
    req['RadiusKm'] = radius
    return json.dumps(req)


if __name__ == "__main__":
    print send_to_query_handler(56.1500, 10.2167, 100)

