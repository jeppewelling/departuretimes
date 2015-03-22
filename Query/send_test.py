import json
from query_service import storage_query_get_stations
from DepartureTimes.communication.send_to_queue import send


if __name__ == '__main__':
    print storage_query_get_stations()
    
    q = {"type": "stations",
         "data": "None"}
    send('storage_import', json.dumps(q))
    
