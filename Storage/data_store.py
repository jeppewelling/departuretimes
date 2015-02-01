from multiprocessing import  Manager

class DataStore(object):
    
    def __init__(self):
        # must be used for shared data
        manager = Manager()
        
        self.stations_index = manager.dict()
        self.cities_index = manager.dict()
        # departures are indexed by station id: Uic
        self.departures_index = manager.dict()

    # Return the stations with their geographical location appended
    # TODO: optimize this
    def get_stations(self):
        print "get_stations: #stations=%r, #cities=%r" % (len(self.stations_index), len(self.cities_index))
        out = []
        s = dict(self.stations_index)
        c = dict(self.cities_index)

        for key in s:
            transformed = transform_stations(c, s[key])
            if transformed == None: continue
            out.append(transformed)
            
        return out




    # Returns a map from station id to list of departures
    def get_departures_from_stations(self, stations):
        departure_map = {}
        for s in stations:
            departure_map[s['Uic']] = self.departures_index[s['Uic']]
            
        return departure_map


    def get_cities():
        print "data_store.get_cities()"
        return self.cities_index

    def add_to_departures_index(self, station_id, departures):
        self.departures_index[station_id] = departures


    def index_stations(self, stations):
        print "index_stations"
        #self.stations_index.clear()
        for s in stations:
            self.stations_index[s['Uic']] = s


    def index_cities(self, cities):
        print "index_cities"
        #self.cities_index.clear()
        for c in cities:
            name = strip_from_city_name(c['Name'])
            self.cities_index[name] = c

    

# Helpers for making station names match with the city names
def remove_end_word(string, endword):
    if string.endswith(endword):
        return string[:-len(endword)]
    return string
                

def strip_from_city_name(city_name):
    city_name = remove_end_word(city_name, " Central")
    city_name = remove_end_word(city_name, "C")
    return city_name.strip()


def transform_stations(cities, s):
    try:
        city = cities[s['Name']]
        return {'Country': s['Country'], 
                'Uic': s['Uic'],
                'Name': s['Name'],
                'Lat' : city['Lat'], 
                'Lon' : city['Lon']}
    except KeyError as ex:
        print "City not found by: %r \n%r" % (s['Name'], ex)
        return None
