import urllib2
import json


# Imports json from a given url.
def import_json(url):
    if url.startswith("https"):
        return import_https_json(url)
    return import_http_json(url)


def import_http_json(url):
    response = urllib2.urlopen(url)
    raw_departures = response.read()
    return json.loads(raw_departures)


def import_https_json(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    raw_output = response.read()
    return json.loads(raw_output)
