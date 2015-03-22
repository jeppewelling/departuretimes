import json
from DepartureTimes.communication.interrupt_handler import message_exception_handler


class ImportServiceMessageHandler(object):
    def __init__(self, data_store, station_publisher, departures_publisher):
        self.data_store = data_store
        self.station_publisher = station_publisher
        self.departures_publisher = departures_publisher

    def on_message_received(self, body):
        with message_exception_handler(body):
            print " [Storage] Message received: %s" % body
            raw = json.loads(body)
            data_type = raw['type']
            data = raw['data']
            if data_type == u'stations':
                self.data_store.index_stations(data)
                self.station_publisher(json.dumps(data))
                return

            if data_type == u'departures':
                from_station = raw['FromStation']
                from_station_id = from_station['Uic']
                self.data_store.add_to_departures_index(from_station_id, data)

                def as_single_departure(from_station_id, data):
                    return {from_station_id: data}

                self.departures_publisher(json.dumps(as_single_departure(from_station_id, data)))

                count = len(data)
                print " [Storage] Received %r departures from %r." % \
                      (count, from_station)

                return

            print " [Import service]: Message type not recognized: %s" % body


