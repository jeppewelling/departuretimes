# -*- coding: utf-8 -*-
import csv
import download_geolocations

file_path = "Data/data/GeoLiteCity_20150106/GeoLiteCity_20150106/GeoLiteCity-Location.csv"

def is_DK_or_SE(row):
    return row[1] == "DK" or row[1] == "SE"


def import_cities_from_csv(csv_path):
    cities = []
    with open(csv_path, 'rb') as csvfile:
        csv_reader = csv.reader(
            csvfile, 
            delimiter=',', 
            quotechar='"')

        for row in csv_reader:
            if len(row) <= 6: continue
            if not is_DK_or_SE(row): continue

            city = {}
            city['Name'] = row[3].decode('latin-1').encode('utf-8')

            # They seriously spelled it: Kjobenhavn
            if "Kjobenhavn" in city['Name']:
                city['Name'] = "København"

            city['Lat'] = row[5].decode('latin-1')
            city['Lon'] = row[6].decode('latin-1')


            cities.append(city)
    return cities


def import_cities():
    download_geolocations.download()
    return import_cities_from_csv(file_path)


if __name__ == "__main__":
    print import_cities()
    
