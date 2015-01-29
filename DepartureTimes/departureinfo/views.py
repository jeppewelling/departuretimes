from django.shortcuts import render
from django.http import HttpResponse
import json
from rmqconnector.send import send_to_query_handler

def index(request, lat):
    return HttpResponse("Hello, world. You're at the polls index.")


def query(request, lat, lon):
    # send to RMQ
    result = send_to_query_handler(lat, lon)
    
    # response...
    return HttpResponse(
        json.dumps(result), 
        content_type="application/json")


def dummy_result(req):
    response_data = {}
    response_data['request'] = req
    response_data['result'] = 'Not available'
    response_data['message'] = 'Stay tuned...'
    return response_data
