# imports packages
from urllib.request import (urlopen)
import json

# empty list
airplane = []

# location of adsb json data from my local antenna
url = "http://adsb.sirver.co:2222/tar1090/data/aircraft.json"

first_response = urlopen(url)

second_response = first_response.read()

json_data = json.loads(second_response)

for data in json_data['aircraft']:
    if {'flight', 'hex', 'alt_baro', 'lat', 'lon'} <= data.keys():
        # print(data['flight'], data['hex'])
        spaced_flight_number = str(data['flight'])
        flight_number = spaced_flight_number.replace(' ', '')
        hex = data['hex']
        altitude = data['alt_baro']
        latitude = data['lat']
        longitude = data['lon']
        dict = {'Hex': hex, 'Flight': flight_number, 'Altitude': altitude, 'Latitude': latitude, 'Longitude': longitude}
        airplane.append(dict)
        # print(hex)
        # airplane.append(flight_number)

print(airplane)

# create json object from the stored adsb list
json_object = json.dumps(airplane, indent=1)

# create the json file from the object
with open("flights.json", "w") as outfile:
   outfile.write(json_object)