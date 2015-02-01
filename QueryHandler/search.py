import math
# Finds the nearest cities

# Calculates the distance between the stations in the list: stations
# and the given point: lat, lon
# returns the stations that are within the given radius.
def get_stations_near(lat, lon, radius, stations):
    station_distances = map(lambda s:
                            { 'Distance' : 
                              distance_between_points(
                                  lat, 
                                  lon, 
                                  float(s['Lat']), 
                                  float(s['Lon'])),
                              'Name' : s['Name'],
                              'Uic' : s['Uic']},
                            stations)
    return filter(
        lambda s: s['Distance'] <= radius, 
        station_distances)





# Thanks to:
# http://andrew.hedges.name/experiments/haversine/
def distance_between_points(lat1, lon1, lat2, lon2):
    # mean radius of the earth (km) at 39 degrees from the equator
    Rk = 6373
    
    t1 = lat1
    n1 = lon1
    t2 = lat2
    n2 = lon2
		
    # convert coordinates to radians
    lat1 = deg2rad(t1)
    lon1 = deg2rad(n1)
    lat2 = deg2rad(t2)
    lon2 = deg2rad(n2)
		
    # find the differences between the coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1
		
    # here's the heavy lifting
    a  = math.pow(math.sin(dlat/2),2) + math.cos(lat1) * math.cos(lat2) * math.pow(math.sin(dlon/2),2)

    # great circle distance in radians
    c  = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a)) 
    # great circle distance in km
    dk = c * Rk 
		
    # round the results down to the nearest 1/1000
    km = round(dk)
    return km

def deg2rad(deg):
    rad = deg * math.pi/180 
    return rad
        

if __name__ == "__main__":
    # Aarhus til Odder
#    print distance_between_points(56.1500,10.2167, 55.9731,10.1530)

    # Aarhus til Hammel
 #   print distance_between_points(56.1500,10.2167, 56.2500,9.8667)

    # stations = [{'Country': u'DK', 'Uic': u'8600032', 'Name': u'Hobro', 'Lat' : 56.6431, 'Lon' : 9.7903},
    #             {'Country': u'DK', 'Uic': u'8600040', 'Name': u'Randers', 'Lat' : 56.4667, 'Lon' : 10.0500},
    #             {'Country': u'DK', 'Uic': u'8600044', 'Name': u'Langaa', 'Lat' : 56.3833, 'Lon' : 9.9000},
    #             {'Country': u'DK', 'Uic': u'8600047', 'Name': u'Hadsten', 'Lat' : 56.3285, 'Lon' : 10.0485},
    #             {'Country': u'DK', 'Uic': u'8600048', 'Name': u'Hinnerup', 'Lat' : 56.2661, 'Lon' : 10.0630},
    #             {'Country': u'DK', 'Uic': u'8600053', 'Name': u'Aarhus', 'Lat' : 56.1567, 'Lon' : 10.2108}]
    # Find nearest cities

    from read_from_storage import storage_query_get_stations
    stations = storage_query_get_stations()
    print stations

    print get_stations_near(56.1500,10.2167, 20, stations)
