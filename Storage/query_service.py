# A service for querying the storage
#
# The storage offers the following queries:
# - get_stations:
#   Get list of stations with geolocations
#
# - get_departures_from_stations:
#   Given a list of stations, return a list of
#   departures from those stations

import json


class QueryServiceMessageHandler(object):
    def __init__(self, data_store):
        self.data_store = data_store

    def on_message_received(self, request):
        request = json.loads(request)
        request_type = request['type']
        print "[Storage: Query service]: Message received: %r" % (request_type)

        if request_type == u"get_stations":
            return json.dumps(self.data_store.get_stations())

        if request_type == u"get_departures":
            stations = request['data']
            return json.dumps(self.data_store.get_departures_from_stations(stations))

        if request_type == u"get_all_departures":
            return json.dumps(self.data_store.get_all_departures())


        print "[Storage: Query service]: Unrecognized request type: %r" % request_type
        return json.dumps(request_type_not_found())


# def make_meta(result, status):
#     meta = {'result': status, 'data': result}
#     return result


def request_type_not_found():
    res = {'message': 'Sorry, the request type ' \
                      'was not recognized. Expected ' \
                      'one of: get_stations, get_departures, get_all_departures'}
    return res
