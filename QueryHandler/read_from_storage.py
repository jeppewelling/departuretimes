import json
from DepartureTimes.communication.rpc_client import RpcClient


def storage_query_get_stations():
    rpc = RpcClient('storage_query')
    q = {}
    q['type'] = "get_stations"
    print q
    return json.loads(rpc.call(json.dumps(q)))

    
def storage_query_get_departures(stations):
    rpc = RpcClient('storage_query')
    q = {}
    q['type'] = "get_departures"
    q['data'] = stations
    return json.loads(rpc.call(json.dumps(q)))
    
    



