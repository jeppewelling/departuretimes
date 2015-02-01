import csv

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
            city['Lat'] = row[5].decode('latin-1')
            city['Lon'] = row[6].decode('latin-1')
            cities.append(city)
    return cities


if __name__ == "__main__":
    print import_cities_from_csv("data/GeoLiteCity-Location.csv")
    

