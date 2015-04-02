import codecs
import json

from django.http import HttpResponse
from setup_rmq import find_departures


def query(request, lat, lon, radius):
    result = find_departures(lat, lon, radius);

    return HttpResponse(
        json.dumps(result),
        content_type="application/json")






def open_json_file(file_path):
    p = None
    with codecs.open(file_path, 'r') as f:
        p = json.load(f)
    f.close();
    return p

def as_places(dict):
    out = []
    for key, places_index in dict.iteritems():
        for place, location in places_index.iteritems():
            out.append({u"Place": place,
                        u"Location": location})
    return out



def places(request):
    return HttpResponse(
        json.dumps(as_places(open_json_file('/srv/departuretimes/places_location.json'))),
        content_type="application/json")



def index(request):
    return HttpResponse("Extend this URL with: /location/&lt;latitude&gt;,&lt;longitude&gt;,&lt;radius in km&gt;")

