import json
from django.shortcuts import render
from django.http import HttpResponse
from send_query import send_to_query_handler
    

def query(request, lat, lon, radius):
    result = send_to_query_handler(lat, lon, radius)

    # response...
    return HttpResponse(
        json.dumps(result), 
        content_type="application/json")


def index(request):
    return HttpResponse("Extend this URL with: /location=&lt;latitude&gt;,&lt;longitude&gt;,&lt;radius in km&gt;")

