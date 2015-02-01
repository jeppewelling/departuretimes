# Deprecated
import math
import store
# Queries to the store

# Returns a map from station id to list of departures
# def get_departures_from_stations(stations):
#     departure_map = {}
#     for s in stations:
#         departure_map[s['Uic']] = store.departures_index[s['Uic']]

#     return departure_map



# # Return the stations with their geographical location appended
# def get_stations():
#     stations_index = store.stations_index
#     cities_index = store.stations_index
    
#     return map(lambda s: 
#                transform_stations(s, cities_index),
#                stations_index)


# def transform_stations(cities, station):
#     city = cities[s['Uic']]
#     return {'Country': s['Country'], 
#             'Uic': s['Uic'],
#             'Name': s['Name'],
#             'Lat' : city['Lat'], 
#             'Lon' : city['Lon']}


if __name__ == "__main__":
    print get_stations()


