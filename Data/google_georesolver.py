from json_url_import import import_json
import json
from urllib import urlencode

api_url = "https://maps.googleapis.com/maps/api/geocode/json?%s&key=AIzaSyBW43vhEDudt_ZEaIlF7-bBKPeSNGW9D-s"

def resolve_address(address):
    url = api_url % address
    return import_json(url)



if __name__ == "__main__":
    addr =  urlencode({ 'address' : "skolebakken st,Denmark"})
    print resolve_address(addr)
