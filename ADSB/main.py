# import urllib library
from urllib.request import urlopen
import time
import os

# import json
import json

# empty array for aircraft data
adsb = []

# store the URL in url as parameter for urlopen
url = "http://adsb.sirver.co:2222/tar1090/data/aircraft.json"

# store the response of URL
response = urlopen(url)

# storing the JSON response from url in data
data_json = json.loads(response.read())

# print the json response
#print(data_json)

# Check the data for flight number and ICAO hex code and store it in a dictionary and then into a list
for a in data_json['aircraft']:
   hex = a.get('hex')
   lat = a.get('lat')
   lon = a.get('lon')
   dirty_flight = a.get('flight')
   if hex and dirty_flight:
      flight_number = dirty_flight.replace(' ','')
      dict = {"Hex": hex, "Flight": flight_number}
      adsb.append(dict)
print(adsb)

# create json object from the stored adsb list
json_object = json.dumps(adsb, indent=1)

# create the json file from the object
with open("flights.json", "w") as outfile:
   outfile.write(json_object)