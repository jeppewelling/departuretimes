import json


class ImportServiceMessageHandler(object):
    def __init__(self, data_store):
        self.data_store = data_store

    def on_message_received(self, body):
        raw = json.loads(body)
        data_type = raw['type']
        data = raw['data']

        if data_type == u'stations':
            print "Storing stations"
            self.data_store.index_stations(data)
            return

        if data_type == u'departures':
            from_station = raw['FromStation']
            from_station_id = from_station['Uic']
            self.data_store.add_to_departures_index(from_station_id, data)
            
            count = len(data)
            print " [x] Received %r departures from %r." % \
                (count, from_station)

            return

        print "[Import service]: Message type not recognized!"

