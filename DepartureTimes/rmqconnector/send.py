import pika
import uuid
import json
from ..communication.rpc_client import RpcClient

queue_name = 'departureinfo_query'

def send_to_query_handler(lat, lon):
    rpc = RpcClient(queue_name)

    print " [x] Requesting %s %s" % (lat, lon)
    response = rpc.call(encode_message(lat, lon))

    print " [.] Got %r" % (response,)
    return response


def encode_message(lat, lon):
    req = {}
    req['lat'] = lat
    req['lon'] = lon
    return json.dumps(req)





