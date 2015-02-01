from django.shortcuts import render
from django.http import HttpResponse
import json

from send_query import send_to_query_handler
    

def query(request, lat, lon):
    result = send_to_query_handler(lat, lon)
    # response...
    return HttpResponse(
        json.dumps(result), 
        content_type="application/json")


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


