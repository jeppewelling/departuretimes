import json
from django.http import HttpResponse
from send_query import find_departures


def query(request, lat, lon, radius):
    result = find_departures(lat, lon, radius)

    return HttpResponse(
        json.dumps(result),
        content_type="application/json")


def index(request):
    return HttpResponse("Extend this URL with: /location=&lt;latitude&gt;,&lt;longitude&gt;,&lt;radius in km&gt;")

