from urllib.request import urlopen
import json
url = "http://adsb.sirver.co:2222/tar1090/data/aircraft.json"

first_response = urlopen(url)

second_response = first_response.read()

json_data = json.loads(second_response)

airplane = []

for data in json_data['aircraft']:
    if 'flight' and 'hex' and 'lat' and 'lon' and 'alt_baro' in data:
        spaced_flight_number = data['flight']
        flight_number = spaced_flight_number.replace(' ','')
        airplane.append(flight_number)

print(flight_number)