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
        print "Message received: %r" % (request_type)

        if request_type == u"get_stations":
            return json.dumps(make_meta(
                self.data_store.get_stations(),
                "Success"))

        if request_type == u"get_departures":
            stations = request['data']
            return json.dumps(make_meta(
                self.data_store.get_departures_from_stations(stations),
                "Success"))

        print "[Query service]: Unrecognized request type: %r" % request_type
        return json.dumps(make_meta(
            request_type_not_found(),
            "Failed"))


def make_meta(result, status):
    meta = {}
    meta['result'] = status
    meta['data'] = result
    return result


def request_type_not_found():
    res = {}
    res['message'] = 'Sorry, the request type '\
                     'was not recoginzed. Expected '\
                     'one of: get_stations, get_departures'
    return res
